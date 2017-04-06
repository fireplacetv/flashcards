from flask_restful import Resource, reqparse
from models import db, Word, Deck, DeckCard

parser = reqparse.RequestParser()
parser.add_argument('english')
parser.add_argument('chinese')

class ApiWords(Resource):
	def get(self):
		words = Word.query.order_by('wid')
		return {
			'did': -1,
			'owner': None,
			'name': 'all words',
			'cards': [w.serialize() for w in words]
		}

	def post(self):
		args = parser.parse_args()
		word = Word(args['english'].lower(), args['chinese'].lower())
		duplicate = Word.query.filter_by(english=args['english'].lower()).filter_by(chinese=args['chinese'])
		if (args['english']=='' or args['chinese']==''):
			return {'result': 'incomplete word', 'word': d.serialize() }, 400
		if duplicate.count() > 0:
			d = duplicate.first()
			return {'result': 'duplicate word', 'word': d.serialize() }, 400
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
		return [w.serialize() for w in words], 200

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
		return word.serialize(), 200

	def delete(self, key):
		word = Word.query.filter_by(wid=key).first()
		if word == None:
			return {'result': 'no match found'}, 404
		db.session.delete(word)
		db.session.commit()
		return {'result': 'success', 'deletedword': word.serialize()}, 200


class ApiDecks(Resource):
	def get(self):
		return 200

	def post(self):
		args = parser.parse_args()
		if (args['uid'] == None or args['name'] == None or args['name']==''):
			return {'result': 'incomplete deck'}, 400
		deck = Deck(args['uid'], args['name'])
		return 200


class ApiDeck(Resource):
	def get(self, key):
		deck = Deck.query.filter_by(did=key).first()
		if (deck == None):
			return {'result': 'no deck found'}, 404
		return deck.serialize(), 200

	def put(self, key):
		deck = Deck.query.filter_by(did=key).first()
		if (deck == None):
			return {'result': 'deck id not found'}, 400
		args=parser.parse_args()
		return 200

	def delete(self, key):
		deck = Deck.query.filter_by(did=key).first()
		if (deck == None):
			return {'result': 'deck id not found'}, 400
		db.session.delete(deck)
		db.session.commit()
		return {'result': 'success'}, 200
