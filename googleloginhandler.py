from basehandler import BaseHandler
import tornado.auth
import tornado.gen
import jwt
from models import User
import datetime

class GoogleLoginHandler(BaseHandler, tornado.auth.GoogleOAuth2Mixin):
    @tornado.gen.coroutine
    def get(self):
        if self.get_argument('code', False):
            user = yield self.get_authenticated_user(redirect_uri=self.settings['redirect_uri'],
                                                     code=self.get_argument('code'))
            data = jwt.decode(user["id_token"], verify=False, algorithms=['RS256'])

            user_id = data['sub']
            email_address = data['email']

            for user in self.db.query(User).filter(User.user_id == user_id):
                self.set_secure_cookie("user", user_id)
                self.redirect('/')
                return

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
        self.set_header("Content-Type", "text/plain")
        first_name = self.get_body_argument('firstname')
        username = self.get_body_argument('username')
        email = self.get_body_argument('email')
        user_id = self.get_body_argument('user_id')
        self.db.add_all([User(user_id=user_id, email=email, date_created=datetime.datetime.utcnow(),
                                         first_name=first_name, username=username)])
        self.set_secure_cookie("user", user_id)
        self.redirect("/")