#!/usr/bin/env python

import webapp2
from controllers.page_controller import PageController
from controllers.book_controller import BookController


#allows method handlers for patch
#http://stackoverflow.com/questions/16280496/patch-method-handler-on-google-appengine-webapp2
allowed_methods = webapp2.WSGIApplication.allowed_methods
new_allowed_methods = allowed_methods.union(('PATCH',))
webapp2.WSGIApplication.allowed_methods = new_allowed_methods

app = webapp2.WSGIApplication([
    ('/', PageController),
    ('/books', BookController),
    ('/books/(.*)', BookController)
], debug=True)
