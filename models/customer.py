from google.appengine.ext import ndb

class Customer(ndb.Model):
	"""Library customer"""
	first_name = ndb.StringProperty()
	last_name = ndb.StringProperty()
