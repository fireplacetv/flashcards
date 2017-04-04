from flask import Flask, render_template, request, session,\
 redirect, url_for, g
from flask_restful import Resource, Api
from models import db, Word
from forms import SignupForm, LoginForm, AddCardForm, EditCardForm, DeleteCardForm
from random import seed,randrange,shuffle
from time import clock
from pinyin import pinyin
import os
from words import ApiAllWords, ApiWord

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('DATABASE_URL')

db.init_app(app)
seed(clock)

#######
# API #
#######
api = Api(app)

api.add_resource(ApiAllWords, '/api/words')
api.add_resource(ApiWord, '/api/words/<int:wid>')


###############
# Flash cards #
###############

def setWidList():
	widlist = [w.wid for w in Word.query.all()]
	shuffle(widlist)
	session['widlist']=widlist

	session['position']=0
	session['pinyin'] = False
	session['language'] = 'chinese'

@app.route("/")
def root():
	session.clear()
	return redirect(url_for('viewCard'))

@app.route("/view/")
@app.route("/view")
def viewCard():
	if 'widlist' in session and 'position' in session:
		wid = session['widlist'][session['position']]
		word = Word.query.filter_by(wid=wid).first()
	else:
		setWidList()
		word = Word.query.filter_by(wid=session['widlist'][0]).first()

	return render_template("view.html",word=word)

@app.route("/view/prev")
def prevCard():
	print session['position']
	session['position']=(session['position'] - 1) % len(session['widlist'])
	print session['position']
	return redirect(url_for('viewCard'))

@app.route("/view/next")
def nextCard():
	session['position']=(session['position'] + 1) % len(session['widlist'])
	return redirect(url_for('viewCard'))

@app.route("/english")
def toggleEnglish():
	session['language'] = 'english'
	return redirect(url_for('viewCard'))

@app.route("/chinese")
def toggleChinese():
	session['language'] = 'chinese'
	return 	redirect(url_for('viewCard'))

@app.route("/pinyin")
def togglePinyin():
	session['language'] = 'pinyin'
	return redirect(url_for('viewCard'))

@app.route("/view/<language>/<translation>")
def viewSpecificCard(language, translation):
	language = language.lower()
	session['language'] = language.lower()
	translation = translation.lower()

	if language == 'english':
		word = Word.query.filter_by(english=translation).first()
	elif language == 'chinese':
		word = Word.query.filter_by(chinese=translation).first()
	elif language == 'wid':
		word = Word.query.filter_by(wid=int(translation)).first()
	else:
		return "couldn't find word"

	if 'widlist' not in session or 'position' not in session:
		setWidList()
	session['position'] = session['widlist'].index(word.wid)

	return render_template("view.html", word=word)

#########################
# Vocabulary management #
#########################

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

@app.route("/delete/<int:wid>", methods=['GET','POST'])
def deleteCard(wid):

	return 'done'

@app.route("/vocabulary", methods=["GET","POST"])
def viewAll():
	vocabulary = Word.query.all();
	form = CardForm()

	if request.method == 'POST':
		if not form.validate():
			return render_template("vocabulary.html", vocabulary=vocabulary, form=form)
		else:
			word = Word(form.english.data.lower(), form.chinese.data.lower())
			db.session.add(word)
			db.session.commit()
			return redirect(url_for("viewAll"))
	elif request.method == 'GET':
		return render_template("vocabulary.html", vocabulary=vocabulary, form=form)



if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0')
