from google.appengine.ext import ndb
import json

class Book(ndb.Model): 
	#determine if an instance is of the book class
	@classmethod
	def is_book(cls, instance):
		return instance.__class__.__name__ == cls.__name__

	#parent key for books in google datastore
	@classmethod
	def parent_key(cls):
		return ndb.Key(cls, "book parent")

	#returns all books
	@classmethod
	def all(cls):
		return cls.query(ancestor=cls.parent_key()).fetch()

	#takes as an argument a list of book instances
	#returns a string which contains a json formatted array of book objects
	@classmethod
	def all_to_json(cls, book_list):
		return json.dumps(map(lambda book: book.to_json_dict(), book_list))
	
	"""Book"""
	title = ndb.StringProperty(required=True)
	isbn = ndb.StringProperty(required=True)
	#genre is an array of strings
	genre = ndb.StringProperty(repeated=True)
	#a book is by default checkedIn when it is created, unless otherwise set
	checkedIn = ndb.BooleanProperty(default=True)


	#returns serialized dictionary of object values
	#with included key
	def to_json_dict(self):
		book_dict = self.to_dict()
		book_dict['id'] = self.key.urlsafe()
		return book_dict

	#returns json formatted string
	def to_json(self):
		return json.dumps(self.to_json_dict())