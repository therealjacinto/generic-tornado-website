#
# basehandler.py: modifies the tornado RequestHandler class for the app. All subsequent handlers overwrite BaseHandler.
#

import tornado.web


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        # Tells the handler where to look to know if the user has logged in and obtained a secure cookie
        return self.get_secure_cookie("user")

    def get(self):
        # Equivalent to using the @tornado.web.authenticated decorator.
        if not self.current_user:
            self.redirect("/login")
            return
        self.render("index.html")
        
    def initialize(self, log, db):
        # Accepts arguments from main.py and saves them in the handler class for use.
        self.log = log
        self.db = db
