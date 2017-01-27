import webapp2

class PageController(webapp2.RequestHandler):
    def get(self):
        self.response.write("hello")