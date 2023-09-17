
from datetime import datetime

from customer import Customer
from inventory import Inventory
from transaction import Transaction
from my_utils import generate_rand

def run(transactions=1, num_customers=1, seasonal_dates=None, num_items=None, discount=0,
        type_of_wine=False, less_than_age_condition=None, greater_than_age_condition=None):
    # This method will walkthrough all necessary functions to generate data

    # 1 .Load products metadata and suppliers
    print('Script Running...')
    customer_list = [Customer() for _ in range(num_customers)]
    inventory = Inventory(data_path = './wine_data/consolidated_wine_data.csv')
    list_of_transactions = []
    filtered_customer_list = []
    
    # 2. Introduce trend parameters
    # 2.1 Filter customer list with discrimination across ages
    if not (less_than_age_condition and greater_than_age_condition):
        print('Applied filter removed all customers. Removing Filter...')
        filtered_customer_list = customer_list
    elif less_than_age_condition:
        filtered_customer_list = [cust for cust in customer_list if cust.dob >= less_than_age_condition]
    elif greater_than_age_condition:
        filtered_customer_list = [cust for cust in customer_list if cust.dob <= greater_than_age_condition]
    else:
        print('No filter applied to customer list.')
        filtered_customer_list = customer_list

    # 3. Option to introduce seasonality  
    if seasonal_dates:
        # format date for consumption
        start_date = datetime(seasonal_dates['y'][0],seasonal_dates['m'][0],seasonal_dates['d'][0])
        end_date = datetime(seasonal_dates['y'][1],seasonal_dates['m'][1],seasonal_dates['d'][1])  
    else:
        start_date = '-3y'
        end_date = 'now'
    time_record = start_date, end_date

    # 3.1 Produce transactions
    for _ in range(transactions):
        for customer in filtered_customer_list:
            # Process transactions
            if not num_items: # number of items each customer buys
                num_items = generate_rand(mean=3, mode=2, prob_of_mode=0.5, sd=1, precision=0)[0]
            shopping_cart= customer.buy_items(number_of_items=num_items,
                                              type_of_wine=type_of_wine,
                                              selection = inventory.list)
            transaction = Transaction(customer, shopping_cart, time_record, discount) # initializes a new session-time and transaction id.
            # Calculate Total
            transaction.get_total() # finalizes transaction and calculates the total value of the transaction (in-place).
            # 4. Update inventory to reflect customer purchases
            inventory.update_inventory(shopping_cart.items)
            list_of_transactions.append((transaction))
    return list_of_transactions 
    

if __name__=='__main__':
    print('Running...')
    sample_transactions = run(transactions=1, num_customers=1)
    
    for transaction in sample_transactions:
        print(transaction)


# To generate some trends: 
# s_dates = {
#    'y':[2022,2022], ->>>>>>['start', 'finish']
#    'm':[5,8],
#    'd':[1,30]
#}

