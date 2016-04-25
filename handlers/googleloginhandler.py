#
# googleloginhandler.py: not to be confused with logouthandler.py. GoogleLoginHandler handles Google OAuth2
# authentication. Once authenticated, the class will check the user against the database, and if the user is a new user,
# they will be redirected to a new user webpage where they enter their name and desired username. Once filled out, they
# are then added to the database.
#
import tornado.auth
import tornado.gen

# Used when adding new user to database
import datetime

# Use for decoding id_token
import jwt

# SQLAlchemy table model used for storing users
from handlers.basehandler import BaseHandler
from models import User


class GoogleLoginHandler(BaseHandler, tornado.auth.GoogleOAuth2Mixin):
    @tornado.gen.coroutine
    def get(self):
        # Taken from tornado's docs. The tornado.auth.GoogleOAuth2Mixin takes care of verifying the user's identity
        # using google endpoints. Custom code begins at "jwt.decode..." and ends at "self.render('new_user.html',..."
        if self.get_argument('code', False):
            user = yield self.get_authenticated_user(redirect_uri=self.settings['redirect_uri'],
                                                     code=self.get_argument('code'))

            # For information on the structure of json web token that Google sends to server, see Google OAuth 2 docs.
            # For this project, we are only interested in the google user id and gmail address. We obtain these from the
            # id token given to us, and store them.
            data = jwt.decode(user["id_token"], verify=False, algorithms=['RS256'])
            user_id = data['sub']
            email_address = data['email']

            # Once the user id has been obtained, it is checked with the database to see if the user is new or not. If
            # the user is not a new user, they are directed to the home page.
            for user in self.db.query(User).filter(User.user_id == user_id):
                self.set_secure_cookie("user", user_id)  # How the server knows the user is logged in
                self.redirect('/')
                return

            # If the user is a new user, they are directed to a new user page where they must create an account.
            self.render('new_user.html', email_address=email_address, user_id=user_id)

        else:
            self.log.info("redirecting")
            yield self.authorize_redirect(
                redirect_uri=self.settings['redirect_uri'],
                client_id=self.settings['google_oauth']['key'],
                scope=['email'],
                response_type='code',
                extra_params={'approval_prompt': 'auto'})

    def post(self):
        # This is used only when the user is a new user. They fill out the form and the fields are passed to the server
        # using the POST method.
        self.set_header("Content-Type", "text/plain")
        first_name = self.get_body_argument('firstname')
        username = self.get_body_argument('username')
        email = self.get_body_argument('email')
        user_id = self.get_body_argument('user_id')

        # The values are then stored into the database and the user is logged in and redirected to the main page
        self.db.add_all([User(user_id=user_id, email=email, date_created=datetime.datetime.utcnow(),
                                         first_name=first_name, username=username)])
        self.set_secure_cookie("user", user_id)  # How the server knows the user is logged in
        self.redirect("/")