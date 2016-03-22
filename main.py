import tornado.ioloop
import tornado.web
import logging

log = logging.getLogger(__name__)

class BaseHandler(tornado.web.RequestHandler):
    def write_error(self, status_code, **kwargs):
        # TODO
        log.debug("DAYUM, SOMETHING TRIPPED")

    def get_current_user(self):
        log.debug("HONKEY")
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
        if not self.get_secure_cookie("mycookie"):
            self.set_secure_cookie("mycookie","myvalue")
            self.write("Your cookie was not set yet!")
        else:
            self.write("Your cookie was set!")


class MainHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        if not self.current_user:
            self.redirect("/login")
            return
        self.render("index.html")

class LoginHandler(BaseHandler):
    def get(self):
        if self.current_user:
            self.redirect("/")
            return
        self.render("login.html")

    def post(self):
        # IMPORTANT: html page must have the input type="text" and name="name"
        self.set_secure_cookie("user", self.get_argument("name"))
        self.redirect("/")

settings = {
    "cookie_secret": "generate_own_random_value",
    "login_url":"/login",
}

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/login", LoginHandler),
    ], **settings)

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()