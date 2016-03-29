from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


def init_db(engine):
    Base.metadata.create_all(bind=engine)


class User(Base):
    __tablename__ = 'users'

    user_id = Column(String(21), primary_key=True)
    email = Column(String(64))
    first_name = Column(String(60))
    username = Column(String(60))
    date_created = Column(DateTime)