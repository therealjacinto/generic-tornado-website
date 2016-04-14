import tornado.ioloop
import tornado.web
from settings import settings

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import models
import datetime

import tornado.auth
import tornado.gen
import jwt

import logging

log = logging.getLogger(__name__)


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        # This is necessary for any calls of self.current_user
        return self.get_secure_cookie("user")

    def get(self):
        if not self.current_user:
            self.redirect("/login")
            return
        self.render("index.html")


class MainHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("index.html")


class LogoutHandler(BaseHandler):
    def get(self):
        def handle_request(response):
            if response.error:
                log.warning("Error, failed in logout")
                log.warning(response.error)
            else:
                log.info("User logged out")

        if self.get_secure_cookie("access_token"):
            access_token = self.get_secure_cookie("access_token")
            revoke_url = 'https://accounts.google.com/o/oauth2/revoke?token=' + access_token.decode("utf-8")
            http_client = tornado.httpclient.AsyncHTTPClient()
            http_client.fetch(revoke_url, handle_request)
            self.clear_cookie("access_token")

        if self.current_user:
            self.clear_cookie("user")

        self.redirect('/login')


class LoginHandler(BaseHandler):
    def get(self):
        self.render("login.html")


class GoogleLoginHandler(BaseHandler, tornado.auth.GoogleOAuth2Mixin):
    @tornado.gen.coroutine
    def get(self):
        if self.get_argument('code', False):
            user = yield self.get_authenticated_user(redirect_uri=self.settings['redirect_uri'],
                                                     code=self.get_argument('code'))
            data = jwt.decode(user["id_token"], verify=False, algorithms=['RS256'])
            # TODO: verify token (https://developers.google.com/identity/protocols/OpenIDConnect#authenticationuriparameters) and
            # (http://stackoverflow.com/questions/17634698/google-oauth-jwt-signature-verification)

            access_token = user['access_token']
            user_id = data['sub']

            def handle_request(response):
                if response.error:
                    log.warning("Invalid Token")
                    log.warning(response.error)
                else:
                    log.info("Token exists")

            validation_url = "https://www.googleapis.com/oauth2/v3/tokeninfo?access_token=" + access_token

            http_client = tornado.httpclient.AsyncHTTPClient()
            validation = http_client.fetch(validation_url, handle_request)

            # validate

            self.set_secure_cookie('access_token', access_token)

            for user in app.session.query(models.User).filter(models.User.user_id==data['sub']):
                self.set_secure_cookie("user", data['sub'])
                self.redirect('/')
                return
            self.render('new_user.html', email_address = data['email'], user_id = data['sub'])


        else:
            yield self.authorize_redirect(
                redirect_uri=self.settings['redirect_uri'],
                client_id=self.settings['google_oauth']['key'],
                scope=['email'],
                response_type='code',
                extra_params={'approval_prompt': 'auto'})

    def post(self):
        self.set_header("Content-Type","text/plain")
        first_name = self.get_body_argument('firstname')
        username = self.get_body_argument('username')
        email = self.get_body_argument('email')
        user_id = self.get_body_argument('user_id')
        app.session.add_all([models.User(user_id=user_id, email=email, date_created=datetime.datetime.utcnow(), first_name=first_name, username=username)])
        self.set_secure_cookie("user", user_id)
        self.redirect("/")

    def _handle_request_exception(self, e):
        self.redirect("/login/google/login_timeout")

class LoginTimeoutHandler(BaseHandler):
    def get(self):
        self.render("login_timeout.html")


class App(tornado.web.Application):
    def __init__(self, handlers=None, default_host="", transforms=None, **web_settings):
        engine = create_engine('sqlite:///:memory:', echo=True)
        models.init_db(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

        super().__init__(handlers, default_host, transforms, **web_settings)


def make_app():
    return App([
        (r"/", MainHandler),
        (r"/login", LoginHandler),
        (r"/logout", LogoutHandler),
        (r"/login/google",GoogleLoginHandler),
        (r"/login/google/login_timeout", LoginTimeoutHandler),
    ], **settings)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()