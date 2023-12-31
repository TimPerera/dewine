"""
`app.py`
This module
"""
from datetime import datetime
import random
from math import ceil
import logging
import os

from utils.logger import SetUpLogging
from dewine.customer import Customer
from dewine.product import Product
from dewine.scene import ScenePlus
from dewine.inventory import Inventory
from dewine.transaction import Transactions
from utils.utils import generate_rand
from config.connection import create_session


SetUpLogging().setup_logging()

logger = logging.getLogger('prod')
session = create_session()


def run(file_path, num_customers=1, seasonal_dates=None, num_items=None, discount=0,
        type_of_wine=False, less_than_age_condition=None, greater_than_age_condition=None, repeat_customers = None):
    # This method will walkthrough all necessary functions to generate data
    # 1 .Load products metadata and suppliers
    logger.info('Script Running...')
    customer_list = [Customer() for _ in range(num_customers)]
    inventory = Inventory(file_path)
    list_of_transactions = []
    filtered_customer_list = []
    
    # 2. Introduce trend parameters
    # 2.1 Filter customer list with discrimination across ages
    if not (less_than_age_condition and greater_than_age_condition):
        logger.debug('No filter applied to customer list.')
        filtered_customer_list = customer_list
    elif less_than_age_condition:
        filtered_customer_list = [cust for cust in customer_list if cust.dob >= less_than_age_condition]
    elif greater_than_age_condition:
        filtered_customer_list = [cust for cust in customer_list if cust.dob <= greater_than_age_condition]
    else:
        logger.debug('Applied filter removed all customers. Removing Filter...')
        filtered_customer_list = customer_list
    
    if repeat_customers:
        number_of_repeat_customers = ceil(repeat_customers * len(filtered_customer_list)) 
        filtered_customer_list.extend(random.sample(filtered_customer_list,number_of_repeat_customers))

    # 3. Option to introduce seasonality  
    if seasonal_dates:
        # format date for consumption
        start_date = datetime(seasonal_dates['y'][0],seasonal_dates['m'][0],seasonal_dates['d'][0])
        end_date = datetime(seasonal_dates['y'][1],seasonal_dates['m'][1],seasonal_dates['d'][1])  
    else:
        logger.debug('No seasonal dates provided.')
        start_date = '-3y'
        end_date = 'now'
    time_record = start_date, end_date

    # 3.1 Produce transactions
    #for _ in range(transactions): # e.g. 10
    for customer in filtered_customer_list: # 5
        # Process transactions
        if not num_items: # number of items each customer buys
            num_items = generate_rand(mean=3, mode=2, prob_of_mode=0.5, sd=1, precision=0)[0]
        shopping_cart= customer.buy_items(number_of_items=num_items,
                                            type_of_wine=type_of_wine,
                                            selection = inventory.items)
        transaction = Transactions(customer, shopping_cart, time_record, discount) # initializes a new session-time and transaction id.
        # Calculate Total
        transaction.get_total() # finalizes transaction and calculates the total value of the transaction (in-place).
        # 4. Update inventory to reflect customer purchases
        inventory.update_inventory(shopping_cart.products)
        list_of_transactions.append((transaction))
    # 4. Upload data to database
    try:
        session.add_all(list_of_transactions)
        session.commit()
        logger.info('Uploaded to SQL Database')
    except Exception as e:
        logger.exception('Database upload failed due to following exception:{}'.format(e))
    return list_of_transactions 
    

if __name__=='__main__':

    script_path = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(script_path,'..', 'data', 'consolidated_wine_data.csv')
    sample_transactions = run(file_path = path,
                              num_customers=2)
    for transaction in sample_transactions:
        print(transaction)
