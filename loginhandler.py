from basehandler import BaseHandler

class LoginHandler(BaseHandler):
    def get(self):
        self.log.info("loaded")
        self.render("login.html")