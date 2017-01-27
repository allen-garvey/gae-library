from google.appengine.ext import ndb
import json

class Book(ndb.Model): 
	"""Book"""
	title = ndb.StringProperty()
	isbn = ndb.StringProperty()
	checked_in = ndb.BooleanProperty()

	def to_json(self):
		book_dict = self.to_dict()
		book_dict['id'] = self.key.urlsafe()
		return json.dumps(book_dict)