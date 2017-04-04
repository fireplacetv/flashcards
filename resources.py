from flask_restful import Resource
from models import db, Word

class ApiAllWords(Resource):
	def get(self):
		words = [{'wid': w.wid, 'english': w.english, 'chinese': w.chinese, 'pinyin': w.pinyin} for w in Word.query.all()]
		return words

class ApiWord(Resource):
	def get(self, wid):
		word = Word.query.filter_by(wid=wid).first()
		return {'wid': wid, 'english': word.english, 'chinese': word.chinese, 'pinyin': word.pinyin}
