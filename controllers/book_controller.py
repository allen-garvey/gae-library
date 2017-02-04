from google.appengine.ext import ndb
import webapp2
import json
from controllers.base_controller import BaseController
from models.book import Book
from models.customer import Customer

class BookController(BaseController):
    #deletes all books
    #note that this won't inspect the integrity of the customer models
    #by removing non-existent books from the checked_out lists, but this will hurt performance,
    #and if you are deleting all the books you probably don't care about
    #data integrity anyway
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


    #edit book, doesn't change non-passed in properties
    #isbn, title, genre and checkIn (to true) are editable
    #if you want to checkout a book, use customer book handler
    def patch(self, book_id):
        #will cause error if customer not found
        try:
            book = ndb.Key(urlsafe=book_id).get()
            #make sure is book and not customer
            assert Book.is_book(book)
        except:
            #not found
            self.response.set_status(404)
            return

        #parse json from request body
        book_data = json.loads(self.request.body)

        #if book is being checked out, send bad request
        #since this should be done using PUT request to 
        # /customers/:customer_id/books/:book_id
        if 'checkedIn' in book_data and book_data['checkedIn'] == False:
            self.response.set_status(400)
            return

        #change editable properties if they are set
        for property_name in ['title', 'isbn', 'genre']:
            if property_name in book_data:
                setattr(book, property_name, book_data[property_name])
        #if book is being checkedIn, make sure to remove it from a customer
        if 'checkedIn' in book_data and book_data['checkedIn'] == True and book.checkedIn == False:
            book.checkedIn = True
            #remove book from customer's checked_out list
            Customer.remove_book(book.key)

        #save book
        book.put()
        #return new book data
        self.write_json(book.to_json())

    #same as patch, but sets attributes to defaults if they are
    #unset in request body
    #checkIn is always set to default value true, since you cannot
    #set checkedIn to false using this handler, should be using the 
    #customer book handler instead
    def put(self, book_id):
        #will cause error if customer not found
        try:
            book = ndb.Key(urlsafe=book_id).get()
            #make sure is book and not customer
            assert Book.is_book(book)
        except:
            #not found
            self.response.set_status(404)
            return

        #parse json from request body
        book_data = json.loads(self.request.body)

        #if book is being checked out, send bad request
        #since this should be done using PUT request to 
        # /customers/:customer_id/books/:book_id
        if 'checkedIn' in book_data and book_data['checkedIn'] == False:
            self.response.set_status(400)
            return

        #change editable properties if they are set
        for property_name, default_value in [('title', ''), ('isbn', ''), ('genre', [])]:
            if property_name in book_data:
                setattr(book, property_name, book_data[property_name])
            else:
                #set to default if not given in requst
                setattr(book, property_name, default_value)
        #since we can't set book checkedIn to false using the PUT handler
        #book will always be set to checkedIn if using PUT
        if book.checkedIn == False:
            book.checkedIn = True
            #remove book from customer's checked_out list
            Customer.remove_book(book.key)

        #save book
        book.put()
        #return new book data
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
                #remove the book from customer's checked_out
                #list, if the book is checked out
                if book.checkedIn == False:
                    Customer.remove_book(book.key)
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