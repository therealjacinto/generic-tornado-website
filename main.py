import tornado.ioloop
import tornado.web

from settings import settings

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import init_db

import logging

from mainhandler import MainHandler
from logouthandler import LogoutHandler
from loginhandler import LoginHandler
from googleloginhandler import GoogleLoginHandler



def make_app():
    # Initialize logger
    log = logging.getLogger(__name__)
    
    # Initialize database
    engine = create_engine('sqlite:///:memory:', echo=True)
    init_db(engine)
    session = sessionmaker(bind=engine)
    db = session()
    
    return tornado.web.Application([
        (r"/", MainHandler, dict(log=log, db=db)),
        (r"/login", LoginHandler, dict(log=log, db=db)),
        (r"/logout", LogoutHandler, dict(log=log, db=db)),
        (r"/login/google", GoogleLoginHandler, dict(log=log, db=db)),
    ], **settings)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()