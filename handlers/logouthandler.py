#
# logouthandler.py: log's user out by clearing their user cookie. NOTE: this app does not also log them out of google.
# When the user logs into the website, they are verifying their identity through Google and thus logging into Google.
# The user must log out of Google themselves if they so desire.
#
from handlers.basehandler import BaseHandler


class LogoutHandler(BaseHandler):
    def get(self):
        # Remove cookie if it exists
        if self.current_user:
            self.clear_cookie("user")

        self.redirect('/login')