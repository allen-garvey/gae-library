from google.appengine.ext import ndb
import webapp2
import json
from controllers.base_controller import BaseController
from models.book import Book
from models.customer import Customer

class CustomerController(BaseController):
    #deletes all customers
    @classmethod
    def delete_all_customers(cls):
        customers = Customer.all()
        for customer in customers:
            ndb.Key(urlsafe=customer.key.urlsafe()).delete()
    
    #if customer_id is given, returns data on specific customer
    #otherwise returns all customers
    def get(self, customer_id=None):
    	#if a customer id is sent, attempt to return the customer
        if customer_id:
            #if customer not found will cause an error
            try:
                customer = ndb.Key(urlsafe=customer_id).get()
                self.write_json(customer.to_json())
            except:
                #error on not found
                self.response.set_status(404)
        #return list of all customers
        else:
            self.write_json(Customer.all_to_json(Customer.all()))

    #create a new customer
    def post(self):
    	#parse json from request body
    	customer_data = json.loads(self.request.body)
        #missing post body information will raise exception, so we need to use try
        try:
            customer = Customer(name=customer_data['name'], parent=Customer.parent_key())
        except:
            #if creating the customer failed, it's most likely due to missing data is post body
            #so just return 'bad request' and exit
            self.response.set_status(400)
            return
    	
        #add optional keys, if they are sent in request body
        for optional_key in ['balance']:
            if optional_key in customer_data:
                setattr(customer, optional_key, customer_data[optional_key])
        #have to set checked_out separately, since we have to convert to ndb.Key instances
        if 'checked_out' in customer_data:
            checked_out = map(lambda book_id: ndb.Key(urlsafe=book_id), customer_data['checked_out'])
            customer.checked_out = checked_out

        #save customer in datastore
    	customer.put()
        #Set HTTP status code to 'created'
    	self.response.set_status(201)
        #return json values of newly created customer
    	self.write_json(customer.to_json())

    #delete a customer by id
    #or all customers
    def delete(self, customer_id=None):
        #delete single book
        if customer_id:
            #if customer not found will cause an error
            try:
                ndb.Key(urlsafe=customer_id).delete()
                #HTTP no content
                self.response.set_status(204)
            except:
                #error on not found
                self.response.set_status(404)
                return
        #delete all customers
        else:
            CustomerController.delete_all_books()
            #HTTP no content
            self.response.set_status(204)
