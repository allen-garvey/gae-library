from google.appengine.ext import ndb
import webapp2
import json
from models.book import Book

class BookController(webapp2.RequestHandler):
    
    #if book_id is given, returns data on specific book
    #otherwise returns all books
    def get(self, book_id=None):
    	#if a book id is sent, return the book
        if book_id:
            #if book not found will cause an error
            try:
                book = ndb.Key(urlsafe=book_id).get()
                self.write_json(book.to_json())
            except:
                #error on not found
                self.response.set_status(404)
        #return list of all books
        else:
            books = map(lambda book: book.to_json_dict(), Book.all())
            self.write_json(json.dumps(books))

    def post(self):
    	#parse json from request body
    	book_data = json.loads(self.request.body)
        #missing post body information will raise exception, so we need to use try
        try:
            book = Book(title=book_data['title'], isbn=book_data['isbn'], parent=Book.parent_key())
        except:
            #if creating the book failed, it's most likely due to missing data is post body
            #so just return 'bad request' and exit
            self.response.set_status(400)
            return
    	
        #add optional keys, if they are sent in request body
        for optional_key in ['checkedIn', 'genre']:
            if optional_key in book_data:
                setattr(book, optional_key, book_data[optional_key])

    	book.put()
        #Set HTTP status code to 'created'
    	self.response.set_status(201)
        #return json values of newly created book
    	self.write_json(book.to_json())

    #convenience method for writing json response
    def write_json(self, json_string):
        self.response.content_type = 'application/json'
        self.response.write(json_string)