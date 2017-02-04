from google.appengine.ext import ndb
import json

class Customer(ndb.Model):
	#parent key for customers in google datastore
	@classmethod
	def parent_key(cls):
		return ndb.Key(cls, "customer parent")

	#returns all customers
	@classmethod
	def all(cls):
		return cls.query(ancestor=cls.parent_key()).fetch()

	#takes as an argument a list of customer instances
	#returns a string which contains a json formatted array of customer objects
	@classmethod
	def all_to_json(cls, customer_list):
		return json.dumps(map(lambda customer: customer.to_json_dict(), customer_list))

	"""Library customer"""
	#customer's full name
	name = ndb.StringProperty(required=True)
	#balance in dollars
	balance = ndb.FloatProperty(default=0)
	#array of book ids
	checked_out = ndb.KeyProperty(repeated=True, kind='Book')


	#returns serialized dictionary of object values
	#with included key
	def to_json_dict(self):
		customer_dict = self.to_dict()
		customer_dict['id'] = self.key.urlsafe()
		#convert checked_out book keys to urls to books
		customer_dict['checked_out'] = map(lambda book_key: '/books/' + book_key.urlsafe(), self.checked_out)
		return customer_dict

	#returns json formatted string
	def to_json(self):
		return json.dumps(self.to_json_dict())
