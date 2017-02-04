from google.appengine.ext import ndb
import webapp2
import json
from controllers.base_controller import BaseController
from models.book import Book
from models.customer import Customer

# functionality getting all of a customer's checked out books
# adding a book to a customer (checking it out) and removing a book
# from a customer (returning the book)
class CustomerBookController(BaseController):

    #returns an array of all books for a customer
    #or data about a single checked out book
    def get(self, customer_id, book_id=None):
        #if customer not found will cause an error
        #or if key of non-customer object (such as a book) will also cause error
        try:
            customer = ndb.Key(urlsafe=customer_id).get()
            #get a single book
            if book_id:
                book = ndb.Key(urlsafe=book_id).get()
                #check to make sure customer checked out this book
                if book.key not in customer.checked_out:
                    #not found
                    self.response.set_status(404)
                    return
                response_data = book.to_json()
            #get all of customer's checked out books
            else:
                books = map(lambda book_key: book_key.get(), customer.checked_out)
                response_data = Book.all_to_json(books)
        except:
            #error on customer not found, or book_id was invalid
            self.response.set_status(404)
            return

        self.write_json(response_data)

    #checkout a book to a customer
    def put(self, customer_id, book_id):
        #if customer or not found will cause an error
        #or if key of non-customer object or non-book object will also cause error
        try:
            customer = ndb.Key(urlsafe=customer_id).get()
            book = ndb.Key(urlsafe=book_id).get()
            #check if book is already checked out
            if book.checkedIn == False:
                #bad request
                self.response.set_status(400)
                return
            #set book to checked out and save
            book.checkedIn = False
            book.put()
            #add book to customer's checked out books and save
            customer.checked_out.append(book.key)
            customer.put()
        except:
            #error on customer not found
            self.response.set_status(404)
            return

        #HTTP created
        self.response.set_status(201)

    #checkin a book from a customer
    def delete(self, customer_id, book_id):
        #if customer or not found will cause an error
        #or if key of non-customer object or non-book object will also cause error
        try:
            customer = ndb.Key(urlsafe=customer_id).get()
            book = ndb.Key(urlsafe=book_id).get()
            #see if customer has checked out this book
            if book.key not in customer.checked_out:
                #bad request
                self.response.set_status(400)
                return
            #set book to checked in and save
            book.checkedIn = True
            book.put()
            #remove book from customer's checked out books and save
            customer.checked_out.remove(book.key)
            customer.put()
        except:
            #error on customer not found
            self.response.set_status(404)
            return

        #HTTP ok
        self.response.set_status(200)