from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = None
Session = None

def init_db(database_url):
    global engine, Session
    engine = create_engine(database_url)
    Session = scoped_session(sessionmaker(bind=engine))
    Base.query = Session.query_property()
    return Session

def get_session():
    if Session is None:
        raise RuntimeError("Database not initialized. Call init_db first.")
    return Session() 