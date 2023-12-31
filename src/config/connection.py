"""
connection.py
This module builds the SQL engine and points it to the correct database to begin populating data.
Works tandem with sql_upload.py.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session
import os 
import logging

from utils.logger import SetUpLogging

SetUpLogging().setup_logging()

logger = logging.getLogger('dev')

script_path = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(script_path,'../..')
logger.debug('Database path:{}'.format(path))
# config_path = os.path.abspath(os.path.dirname(os.path.dirname(dir_path)))
# src_path = os.path.dirname(config_path)
# logger.info('Came here')
# logger.debug(src_path)


#import configparser

class Base(DeclarativeBase):
    pass

#config = configparser.ConfigParser()
#config.read('config.ini')
#db_url = 'postgresql://postgres:dewine@localhost/dewine'
#engine = create_engine(db_url, echo=True)
engine = create_engine(f"sqlite:///{path}/dewine.db",echo=False)
# Create tables
def create_session():
    Base.metadata.create_all(engine) # engine define in globally
    session = Session(bind=engine)
    return session

