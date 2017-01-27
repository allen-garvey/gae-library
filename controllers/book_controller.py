from google.appengine.ext import ndb
import webapp2
import json
from models.book import Book

class BookController(webapp2.RequestHandler):
    def get(self, book_id=None):
    	if book_id:
        	book = ndb.Key(urlsafe=book_id).get()
        	self.response.write(book.to_json())
        else:
        	self.response.write("hello from books")

    def post(self):
    	book_parent_key = ndb.Key(Book, "book parent")
    	#parse json from request body
    	book_data = json.loads(self.request.body)
    	book = Book(title=book_data['title'], isbn=book_data['isbn'], checked_in=False, parent=book_parent_key)
    	#save in cloud datastore
    	book.put()
    	self.response.set_status(201)
    	self.response.write(book.to_json())