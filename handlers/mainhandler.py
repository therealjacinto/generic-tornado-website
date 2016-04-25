#
# mainhandler.py: renders main page and displays custom text on page for user.
#

import tornado.web

# Database models
from handlers.basehandler import BaseHandler
from models import User


class MainHandler(BaseHandler):
    @tornado.web.authenticated  # Redirect to login page if cookie is not set.
    def get(self):
        # Get first name of user from database using user id in cookie
        name = ""
        for user in self.db.query(User).filter(User.user_id == self.get_current_user().decode("utf-8")):
            name = " " + user.first_name

        self.render("index.html", name=name)
