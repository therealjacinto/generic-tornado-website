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
    def write_error(self, status_code, **kwargs):
        # TODO
        log.debug("DAYUM, SOMETHING TRIPPED")

    def get_current_user(self):
        # This is necessary for any calls of self.current_user
        return self.get_secure_cookie("user")

    def prepare(self):
        # TODO
        log.debug("Prepare Yo-Self!")

    def on_connection_close(self):
        # TODO - called when the client disconnects; applications may choose to detect this case
        # and halt further processing. Note that there is no guarantee that a closed connection
        # can be detected promptly.
        log.debug("User has left the building!")

    def get(self):
        if not self.current_user:
            self.redirect("/login")
            return
        self.render("index.html")


class MainHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("index.html")


class NewUserHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("new_user.html")


class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.redirect('/login')


class LoginHandler(BaseHandler, tornado.auth.GoogleOAuth2Mixin):
    @tornado.gen.coroutine
    def get(self):
        if self.get_argument('code', False):
            user = yield self.get_authenticated_user(redirect_uri=self.settings['redirect_uri'],
                                                     code=self.get_argument('code'))
            data = jwt.decode(user["id_token"], verify=False, algorithms=['RS256'])
            # TODO: verify token (https://developers.google.com/identity/protocols/OpenIDConnect#authenticationuriparameters) and
            # (http://stackoverflow.com/questions/17634698/google-oauth-jwt-signature-verification)

            for user in app.session.query(models.User).filter(models.User.user_id==data['sub']):
                self.set_secure_cookie("user", data['sub'])
                self.redirect('/')
                return
            app.session.add_all([models.User(user_id=data['sub'], email=data['email'], date_created=datetime.datetime.utcnow())])
            self.set_secure_cookie("user", data['sub'])
            self.redirect('/new')


        else:
            yield self.authorize_redirect(
                redirect_uri=self.settings['redirect_uri'],
                client_id=self.settings['google_oauth']['key'],
                scope=['email'],
                response_type='code',
                extra_params={'approval_prompt': 'auto'})


class FIBApplication(tornado.web.Application):
    def __init__(self, handlers=None, default_host="", transforms=None, **web_settings):
        engine = create_engine('sqlite:///:memory:', echo=True)
        models.init_db(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

        super().__init__(handlers, default_host, transforms, **web_settings)


def make_app():
    return FIBApplication([
        (r"/", MainHandler),
        (r"/login", LoginHandler),
        (r"/new", NewUserHandler),
        (r"/logout", LogoutHandler)
    ], **settings)


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()