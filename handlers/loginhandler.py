#
# loginhandler.py: not to be confused with googleloginhandler.py. This handler only renders the custom login page for
# the website. It does not handle authentication (see googleloginhandler).
#
from handlers.basehandler import BaseHandler


class LoginHandler(BaseHandler):
    def get(self):
        self.render("login.html")