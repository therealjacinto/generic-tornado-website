import tornado.web

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        # This is necessary for any calls of self.current_user
        return self.get_secure_cookie("user")

    def get(self):
        if not self.current_user:
            self.redirect("/login")
            return
        self.render("index.html")
        
    def initialize(self, log, db):
        self.log = log
        self.db = db