"""
sql_upload.py
This module provides functionality to upload generated data to a SQL Database.
"""
from app import run
from connection import create_session, engine

session = create_session()
num_customers = 1

# get transaction list
transaction_list = run(
        file_path='./wine_data/consolidated_wine_data.csv',
        num_customers=num_customers, 
        repeat_customers=0.3)


print(transaction_list[0])
# get customer list
#session.add_all(transaction_list)

#session.commit()