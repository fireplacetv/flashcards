from flask import Flask, render_template, request, session, redirect, url_for
from models import db, Word
from forms import SignupForm, LoginForm, CardForm
from random import seed,randrange
from time import clock
from pinyin import pinyin

app = Flask(__name__)

app.secret_key = "development-key"

app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://localhost/flashr'
db.init_app(app)

seed(clock)

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/add", methods=["GET","POST"])
def addCard():
	form = CardForm()

	if request.method == 'POST':
		if not form.validate():
			return render_template("add.html", form=form)	
		else:
			word = Word(form.english.data.lower(), form.chinese.data.lower())
			db.session.add(word)
			db.session.commit()

			return redirect(url_for("viewCard", language='chinese',translation=form.chinese.data))

	elif request.method == 'GET':
		return render_template("add.html", form=form)

@app.route("/edit/<wid>", methods=['GET','POST'])
def editCard(wid):
	word = Word.query.get(wid)
	if word == None:
		return redirect(url_for('addCard'))

	form = CardForm(obj=word);

	if request.method == 'POST':
		if not form.validate():
			return render_template("edit.html", word=word, form=form)
		else:
			Word.query.get(wid).update(dict(english=form.english.data.lower(),chinese=form.chinese.data.lower(),pinyin=pinyin(form.chinese.data)))

	elif request.method == 'GET':
		return render_template("edit.html", word=word, form=form)

@app.route("/view/<language>/<translation>")
def viewCard(language, translation):
	language = language.lower()
	translation = translation.lower()

	print language,translation

	if language == 'english':
		word = Word.query.filter_by(english=translation).first()
		return render_template("view.html", language=language, word=word)
	elif language == 'chinese':
		word = Word.query.filter_by(chinese=translation).first()
		return render_template("view.html", language=language, word=word)
	else:
		return "couldn't find word"


if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0')
