import tornado.ioloop
import tornado.web
import logging
import tornado.auth
import tornado.gen
import jwt
from settings import settings

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


class LoginHandler(BaseHandler, tornado.auth.GoogleOAuth2Mixin):
    @tornado.gen.coroutine
    def get(self):
        # if self.current_user:
        #     self.redirect("/")
        #     return
        # self.render("login.html")

        if self.get_argument('code', False):
            user = yield self.get_authenticated_user(redirect_uri=self.settings['redirect_uri'],
                                                     code=self.get_argument('code'))
            data = jwt.decode(user["id_token"], verify=False, algorithms=['RS256'])
            # TODO: verify token (https://developers.google.com/identity/protocols/OpenIDConnect#authenticationuriparameters) and
            # (http://stackoverflow.com/questions/17634698/google-oauth-jwt-signature-verification)

            # self.write(data)
            self.set_secure_cookie("user", data['sub'])
            self.redirect('/')

        else:
            yield self.authorize_redirect(
                redirect_uri=self.settings['redirect_uri'],
                client_id=self.settings['google_oauth']['key'],
                scope=['email', 'profile'],
                response_type='code',
                extra_params={'approval_prompt': 'auto'})

    # def post(self):
    #     # IMPORTANT: html page must have the input type="text" and name="name"
    #     self.set_secure_cookie("user", self.get_argument("name"))
    #     self.redirect("/")


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/login", LoginHandler),
    ], **settings)


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()