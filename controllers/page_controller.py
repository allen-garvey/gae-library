import webapp2
from controllers.book_controller import BookController
from controllers.customer_controller import CustomerController

class PageController(webapp2.RequestHandler):
    def get(self):
        self.response.write("hello")

    #delete all books and all customers
    def delete(self):
    	BookController.delete_all_books()
    	CustomerController.delete_all_customers()
    	#HTTP no content
        self.response.set_status(204)