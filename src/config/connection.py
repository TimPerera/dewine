"""
connection.py
This module builds the SQL engine and points it to the correct database to begin populating data.
Works tandem with sql_upload.py.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session
#import configparser

class Base(DeclarativeBase):
    pass

#config = configparser.ConfigParser()
#config.read('config.ini')
#db_url = 'postgresql://postgres:dewine@localhost/dewine'
#engine = create_engine(db_url, echo=True)
engine = create_engine("sqlite:///dewine.db",echo=False)
# Create tables
def create_session():
    Base.metadata.create_all(engine) # engine define in globally
    session = Session(bind=engine)
    return session
