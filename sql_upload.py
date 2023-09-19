"""
sql_upload.py
This module provides functionality to upload generated data to a SQL Database.
"""

# when a transaction is made, we need to update the following:
# transaction history 
# client's pocket
# inventory

# 1) Build the transaction history table
# 2) For each transaction we can get data about the clients
# 3) Once all the transactions have been processed we just 
# need to copy the inventory data and write it to a table
from app import run
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import configparser


config = configparser.ConfigParser()
config.read('config.ini')

db_url = config['database']['db_url']
engine = create_engine(db_url)
Session = sessionmaker(bind=engine)
session = Session()

num_customers = 5

# get transaction list
transaction_list =   run(
        file_path='./wine_data/consolidated_wine_data.csv',
        num_customers=num_customers, 
        repeat_customers=0.3)

# get customer list
for transaction in transaction_list:
    print(transaction.customer)