import tornado.web
from basehandler import BaseHandler
from models import User

class MainHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        name = " "
        for user in self.db.query(User).filter(User.user_id == self.get_current_user().decode("utf-8")):
            name = name + user.first_name
        self.render("index.html", name=name)