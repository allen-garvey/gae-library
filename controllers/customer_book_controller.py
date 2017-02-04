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
    def get(self, customer_id):
        #if customer not found will cause an error
        #or if key of non-customer object (such as a book) will also cause error
        try:
            customer = ndb.Key(urlsafe=customer_id).get()
            books = map(lambda book_key: book_key.get(), customer.checked_out)
        except:
            #error on customer not found
            self.response.set_status(404)
            return

        self.write_json(Book.all_to_json(books))
