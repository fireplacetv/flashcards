from flask.ext.sqlalchemy import SQLAlchemy
from pinyin import pinyin
from json import dumps

db = SQLAlchemy()

class Word(db.Model):
	__tablename__ = "words"
	wid = db.Column(db.Integer, primary_key = True)
	english = db.Column(db.String(60))
	chinese = db.Column(db.String(60))
	pinyin = db.Column(db.String(60))

	def __init__(self, english, chinese):
		self.english = english
		self.chinese = chinese
		self.pinyin = pinyin.get(chinese)

	def setEnglish(english):
		self.english = english

	def setChinese(chinese):
		self.chinese = chinese
		self.pinyin = pinyin.get(chinese)

	def serialize(self):
		return {
			'english': self.english,
			'chinese': self.chinese,
			'pinyin': self.pinyin
		}