import webapp2
import json

#base controller class
class BaseController(webapp2.RequestHandler):

#convenience method for writing json response
    def write_json(self, json_string):
        self.response.content_type = 'application/json'
        self.response.write(json_string)