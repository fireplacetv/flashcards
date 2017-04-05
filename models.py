from flask_sqlalchemy import SQLAlchemy
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

	def setEnglish(self, english):
		self.english = english

	def setChinese(self, chinese):
		self.chinese = chinese
		self.pinyin = pinyin.get(chinese)

	def serialize(self):
		return {
			'english': self.english,
			'chinese': self.chinese,
			'pinyin': self.pinyin
		}

class User(db.Model):
	__tablename__ = "users"
	uid = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(60), unique=True)
	password = db.Column(db.String(120))

	def __init__(self, email, pssword):
		self.email = email
		self.password = password

	def serialize(self):
		return {
			'email': self.email,
			'password': self.password
		}

class Deck(db.Model):
	__tablename__ = "decks"
	did = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(60))
	owner = db.Column(db.Integer, db.ForeignKey('users.uid'))

	def __init__(self, name, ownerId):
		self.name = name
		self.owner = ownerId

class DeckCards(db.Model):
	__tablename__ = "deckcards"
	dcid = db.Column(db.Integer, primary_key = True)
	did = db.Column(db.Integer, db.ForeignKey('decks.did'))
	wid = db.Column(db.Integer, db.ForeignKey('words.wid'))

	def __init__(self, deckId, wordId):
		self.did = deck
		self.wid = word
