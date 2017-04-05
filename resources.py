from flask_restful import Resource, reqparse
from models import db, Word

parser = reqparse.RequestParser()
parser.add_argument('english')
parser.add_argument('chinese')

class ApiAllWords(Resource):
	def get(self):
		words = Word.query.all()
		return [{'wid': w.wid, 'english': w.english, 'chinese': w.chinese, 'pinyin': w.pinyin} for w in words]

	def post(self):
		args = parser.parse_args()
		word = Word(args['english'].lower(), args['chinese'].lower())
		duplicate = Word.query.filter_by(english=args['english'].lower()).filter_by(chinese=args['chinese'])
		if duplicate.count() > 0:
			d = duplicate.first()
			return {'result': 'duplicate word', 'word': {'wid': d.wid, 'english': d.english, 'chinese': d.chinese, 'pinyin': d.pinyin}}, 400
		else: 
			db.session.add(word)
			db.session.commit()
			return word, 201

class ApiWord(Resource):
	def get(self, key):
		if (key==''):
			return redirect(url_for('api.allwords'))
		words = Word.query.filter_by(english=key)
		if words.count()==0:
			words = Word.query.filter_by(chinese=key)
		if words.count()==0:
			words = Word.query.filter_by(wid=key)
		if words.count()==0:
			return {'result': 'no matches found'}, 404
		return [{'wid': w.wid, 'english': w.english, 'chinese': w.chinese, 'pinyin': w.pinyin.lower()} for w in words]

	def put(self, key):
		word = Word.query.filter_by(wid=key).first()
		if word == None:
			return {'result': 'no match found'}, 404
		args = parser.parse_args()
		if 'english' in args.keys() and args['english'] != None:
			word.setEnglish(args['english'])
		if 'chinese' in args.keys() and args['chinese'] != None:
			word.setChinese(args['chinese'])
		db.session.commit()
		return {'wid': word.wid, 'english': word.english, 'chinese': word.chinese, 'pinyin': word.pinyin}, 200


	def delete(self, key):
		word = Word.query.filter_by(wid=key).first()
		if word == None:
			return {'result': 'no match found'}, 404
		wordJSON = {'wid': word.wid, 'english': word.english, 'chinese': word.chinese, 'pinyin': word.pinyin}
		db.session.delete(word)
		db.session.commit()
		return {'result': 'success', 'deletedword': wordJSON}, 200

class ApiDeck(Resource):
	def get(self):
		return 200

	def post(self):
		return 200

