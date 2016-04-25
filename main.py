#
# main.py: handles web application initialization and deployment. For more information on how a tornado web app should be
# set up, visit the tornado docs to read more.
#

# Import necessary tornado files for server application
import tornado.ioloop
import tornado.web

# Import tornado settings for cookie secret, @authenticated redirect page, google oauth credentials and redirect uri,
# xsrf cookies, and the designated paths for static files and templates. See wiki for example.
from settings import settings

# Import necessary files for creating and maintaining a database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import init_db

# Necessary for debugging
import logging

# Created handlers that perform backend duties
from handlers.mainhandler import MainHandler  # handles home page
from handlers.logouthandler import LogoutHandler  # handles logging out and redirects to login page
from handlers.loginhandler import LoginHandler  # handles login page and redirects to google oauth process
from handlers.googleloginhandler import GoogleLoginHandler  # handles google oauth and handles database addition for new user


# Function that initializes logger and database and creates a web application using these and the imported settings
def make_app():
    # Setup module-level logging
    log = logging.getLogger(__name__)
    # Allow log to show debug level messages
    logging.basicConfig(level=logging.DEBUG)
    
    # Create database object (see SQLAlchemy website for more information)
    engine = create_engine('sqlite:///:memory:', echo=False)  # If you want to see messages in terminal, set "echo=True"
    init_db(engine)
    session = sessionmaker(bind=engine)
    db = session()

    # Create application object. Database and log are added as an argument in each handler to give it the option of
    # using it. In this project, they are not all used in each handler.
    return tornado.web.Application([
        (r"/", MainHandler, dict(log=log, db=db)),
        (r"/login", LoginHandler, dict(log=log, db=db)),
        (r"/logout", LogoutHandler, dict(log=log, db=db)),
        (r"/login/google", GoogleLoginHandler, dict(log=log, db=db)),
        (r"/(.*)", MainHandler, dict(log=log, db=db))
    ], **settings)


if __name__ == "__main__":
    # Create and deploy app
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
