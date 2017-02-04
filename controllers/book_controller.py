from google.appengine.ext import ndb
import webapp2
import json
from controllers.base_controller import BaseController
from models.book import Book

class BookController(BaseController):
    #deletes all books
    @classmethod
    def delete_all_books(cls):
        books = Book.all()
        for book in books:
            ndb.Key(urlsafe=book.key.urlsafe()).delete()
    
    #if book_id is given, returns data on specific book
    #otherwise returns all books
    def get(self, book_id=None):
    	#if a book id is sent, return the book
        if book_id:
            #if book not found will cause an error
            try:
                book = ndb.Key(urlsafe=book_id).get()
                #make sure is book and not customer
                assert Book.is_book(book)
                self.write_json(book.to_json())
            except:
                #error on not found
                self.response.set_status(404)
        #return list of all books
        else:
            #if request parameter not sent, will be empty string
            #convert to lowercase so we get case insensitive string comparison
            #http://stackoverflow.com/questions/319426/how-do-i-do-a-case-insensitive-string-comparison-in-python
            checked_out_parameter = self.request.get('checkedIn').lower()
            #just show books that are not checked in
            if checked_out_parameter == 'false':
                books = Book.query(Book.checkedIn == False).fetch()
            #just show books that are checkedIn
            elif checked_out_parameter == 'true':
                books = Book.query(Book.checkedIn == True).fetch()
            #show all books
            else:
                books = Book.all()
            self.write_json(Book.all_to_json(books))

    #create a new book
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

        #save book in datastore
    	book.put()
        #Set HTTP status code to 'created'
    	self.response.set_status(201)
        #return json values of newly created book
    	self.write_json(book.to_json())

    #delete a book by id
    #or all books
    def delete(self, book_id=None):
        #delete single book
        if book_id:
            #if book not found will cause an error
            try:
                book = ndb.Key(urlsafe=book_id).get()
                #make sure is book
                assert Book.is_book(book)
                #delete the book
                ndb.Key(urlsafe=book_id).delete()
                #HTTP no content
                self.response.set_status(204)
            except:
                #error on not found
                self.response.set_status(404)
                return
        #delete all books
        else:
            BookController.delete_all_books()
            #HTTP no content
            self.response.set_status(204)