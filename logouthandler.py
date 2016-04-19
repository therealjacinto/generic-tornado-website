from basehandler import BaseHandler

class LogoutHandler(BaseHandler):
    def get(self):
        if self.current_user:
            self.clear_cookie("user")

        self.redirect('/login')