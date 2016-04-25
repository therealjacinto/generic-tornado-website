#
# models.py: contains the SQLAlchemy model for the database table that stores users. For more information on how a model
# is setup, visit the SQLAlchemy website.
#

# SQLAlchemy files for base and table creation
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# Initializing database and binding engine using declarative base above
def init_db(engine):
    Base.metadata.create_all(bind=engine)


# Table used for databasing users. The user_id is taken from google oauth and stored as the primary key. Because the
# id is too big for a BIGINT, it is stored as a string. Email is also taken from google oauth, but the first name and
# username are both provided by the user when they first log into the website using their google account.
class User(Base):
    __tablename__ = 'users'

    user_id = Column(String(21), primary_key=True)
    email = Column(String(64))
    first_name = Column(String(60))
    username = Column(String(60))
    date_created = Column(DateTime)
