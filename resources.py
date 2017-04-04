from flask_restful import Resource, reqparse
from models import db, Word

parser = reqparse.RequestParser()
parser.add_argument('english')
parser.add_argument('chinese')

class ApiAllWords(Resource):
	def get(self):
		words = [{'wid': w.wid, 'english': w.english, 'chinese': w.chinese, 'pinyin': w.pinyin} for w in Word.query.all()]
		return words

	def post(self):
		args = parser.parse_args()
		word = Word(args['english'].lower(), args['chinese'].lower())
		db.session.add(word)
		db.session.commit()
		return word, 201

class ApiWord(Resource):
	def get(self, wid):
		word = Word.query.filter_by(wid=wid).first()
		return {'wid': wid, 'english': word.english, 'chinese': word.chinese, 'pinyin': word.pinyin}

	def put(self, wid):
		return 'nothing yet'

	def delete(self, wid):
		word = Word.query.filter_by(wid=wid).first()
		db.session.delete(word)
		db.session.commit()
		return '', 204
