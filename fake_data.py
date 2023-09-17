# pump data into databases

# customer
# credentials
# customerLocation
# contact
# creditCardPayment
# orderTable
# scenePlus
# payment
# orderDetails
# orderStatus
# session
# shoppingCart
# discount
# supplier
# product
# inventory

from datetime import timedelta
from datetime import datetime
from faker import Faker
import bcrypt
import random
import numpy as np
import pandas as pd
import uuid
from math import ceil
from dateutil.relativedelta import relativedelta
from collections import defaultdict

# customer
fake = Faker()

def hash_pw(password):
    # secures password via salting
    salt = bcrypt.gensalt()
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'),salt)
    return hashed_pw

def generate_rand(mean,mode, prob_of_mode, sd=1, size = 1,precision=2, non_zero = True):
    # a function that generates values based on a specified distribution.
    # value returned will always be positive.
    res = []
    rand_val = 0
    for _ in range(size):
        if non_zero:
            while rand_val == 0:
                rand_val = random.gauss(mu=mean,sigma=sd)
        if random.random() <= prob_of_mode:
            if precision == 0:
                res.append(ceil(abs(mode)))
            else:
                res.append(abs(round(mode,precision)))
        else:
            if precision == 0:
                res.append(abs(ceil(round(rand_val, precision))))
            else:
                res.append(abs(round(rand_val,precision)))
    return res

class ShoppingCart():
    #  Generates a ShoppingCart option which contains the shopped items along with a time stamp. 
    def __init__(self, items):
        self.items = items
        self.cart_id = uuid.uuid4()

    def __len__(self):
        return len(self.items)

    def  __str__(self):
        # What is called when a ShoppingCart object is called. 
        return f"""
        Cart_ID: {self.cart_id}
        Total Cart Items: {len(self.items)}
        Cart Instantiated at: {self.session_start_time}
        """


class Product():
    # Generates an instance of a product with all its details.
    def __init__(self):
        self.idx = None
        self.type = None
        self.name = None
        self.winery = None
        self.country = None
        self.region = None
        self.quantity = 0
        self.price = None
        self.year = None
        self.inventory = 0

    def load_products(self, data):
        for id, product in enumerate(data.itertuples()):
            self.type = product.Type
            self.idx = id
            self.name = product.Name
            self.winery = product.Winery
            self.region = product.Region
            self.rating = product.Rating
            self.price = product.Price
            self.year = product.Year
            self.inventory = generate_rand(mean=600, mode=550, prob_of_mode=0.5, sd=1.2, size=1,precision=0)[0]
        print('Products Loaded.')
        
    
    def __str__(self):
        return f'''
        Product ID: {self.idx}
        Product Name: {self.name}
        Product Winery: {self.winery}
        Product Year: {self.year}
        Product Price: {self.price}
        '''

class Customer():
    # Generates an instance of a customer with all their details. 
    def __init__(self):

        self.first_name = fake.first_name()
        self.last_name = fake.last_name()
        self.dob = fake.date_of_birth(minimum_age = 18, maximum_age=90)
        self.scene_ID = fake.unique.random_int(min=1, max=999999)
        self.password = hash_pw(fake.password())
        self.full_address = fake.address()
        self.city = fake.city()
        self.postal_code = fake.postalcode()
        self.email = str.lower(self.first_name) + '.' +str.lower(self.last_name) + '@' + fake.free_email_domain()
        self.phone = fake.phone_number()
        self.credit_card = fake.credit_card_full(card_type='mastercard')
        self.credit_card_expiry = fake.credit_card_expire()
        self.store_credit = generate_rand(mean=5, mode=0, prob_of_mode = 0.8, size = 1, precision = 2)[0]
        self.scene_points = generate_rand(mean=1000,mode=700,prob_of_mode=0.7,size=1)[0]

    def buy_items(self, number_of_items=1, bias=True, type_of_wine= None, selection = None):
        # Fetches a product along with all its details. 
        # This method replicates the action of a customer selecting products (with varying quantities)
        # create purchasing bias towards higher rated wines
        # selection refers to the product selection available to the client when shopping
        cart = ShoppingCart(items=[])
        high_rated_products = low_rated_products = []
        if type_of_wine:
            high_rated_products = [product for product in selection if (type_of_wine is None and product.rating > 4.4) or (type_of_wine is not None and product.rating > 4.4 and product.type == type_of_wine)]
            low_rated_products = [product for product in selection if (type_of_wine is None and product.rating <= 4.4) or (type_of_wine is not None and product.rating <= 4.4 and product.type == type_of_wine)]
        else:
            high_rated_products = [product for product in selection if product.rating > 4.4]
            low_rated_products = [product for product in selection if product.rating <= 4.4]
        threshold =  0.7 if bias else 0.5
        product_chosen = None
        for _ in range(number_of_items):
            quantity = generate_rand(mean = 2,mode = 1, prob_of_mode=0.8, size=1, precision=0)[0]
            if random.gauss(0,1) < threshold:
                product_chosen = random.choice(high_rated_products)
                product_chosen.quantity = quantity
            else:
                product_chosen = random.choice(low_rated_products)
                product_chosen.quantity = quantity
            cart.items.append(product_chosen)
        return cart
        
    def __str__(self):
        # What is printed out when a customer instance is called. 
        return f''' 
        Customer SceneID = {self.scene_ID}
        Name: {" ".join([self.first_name, self.last_name])}
        Address: {self.full_address}
        Email: {self.email}
        Phone: {self.phone}
        Payment Method Available: {self.credit_card is not None}
        Store Credit: ${self.store_credit}
        Scene Points: {self.scene_points}
            '''

class Inventory():
    def __init__(self, data_path):
        # Upon initialization loads data 
        data = pd.read_csv(data_path)
        self.list = self.populate_inventory(data)

    def update_inventory(self, cart):
        # Updates inventory, negative values represent pre-orders for once stocks become available.
        # TODO: Make SQL call to update inventory table
        for product in cart:
            product.inventory -= product.quantity # remove ordered items from inventory
            if product.inventory <= 5: 
                print(f"Warning Low Inventory for {product.idx}: {product.name}")
        print("Inventory updated")

    def populate_inventory(self, wine_data):
        # Generate product info
        product_list = []
        for id, data in enumerate(wine_data.itertuples()):
            product = Product()
            product.type = data.Type
            product.idx = id
            product.name = data.Name
            product.winery = data.Winery
            product.region = data.Region
            product.rating = data.Rating
            product.price = data.Price
            product.year = data.Year
            product.inventory = generate_rand(mean=600, mode=550, prob_of_mode=0.5, sd=1.2, size=1,precision=0)[0]
            product_list.append(product)
        print('Database uploaded.')
        return product_list

class Transaction():

    def __init__(self, customer, cart, time_limits, discount=0):
        self.discount = discount
        self.customer = customer
        self.cart = cart
        self.session_time = self.generate_session_time(time_limits)
        self.transaction_id = self.generate_transaction_id()
        self.discount_total = self.get_discount(self.discount)
        self.total_cost = self.get_total() - self.discount_total

    def __repr__(self):
        customer_name = f"{self.customer.first_name + ' ' + self.customer.last_name}"
        customer_age = relativedelta(datetime.now().date(), self.customer.dob).years
        items_purchased = len(self.cart)
        products = [product.name for product in self.cart.items]

        return f'''
        Transaction Details:
        Date: {self.session_time}
        Customer: {customer_name}
        Customer Age: {customer_age} years
        Items Purchased: {items_purchased}
        Total Cost: ${self.total_cost}
        Total Discount Applied: ${self.discount_total}
        Products: {products}
        '''

    def generate_session_time(self, time_limits):
        start_date, end_date = time_limits
        session_start_time = fake.date_time_between(start_date = start_date, end_date = end_date)
        return session_start_time

    def generate_transaction_id(self):
        transaction_id = fake.unique.random_int(min=111111, max=999999)
        return transaction_id

    def get_total(self):
        total_price = 0
        for product in self.cart.items:
            total_price += product.price * product.quantity 
        total_price = round(total_price,2)
        return total_price
    
    def get_discount(self, discount):
        return discount*self.get_total()


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
    

if __name__=='main':
    print('Running...')
    sample_transactions = run(transactions=1, num_customers=1)
    
    for transaction in sample_transactions:
        print(transaction)


    # generate data pertaining to transactions - DONE
    # produce_transactions(transactions = 5)
    # print('Complete!')
    # generate normal data across most of the products, 5% should have no sales.
    # generate random `number_of_items` outliers
    # produce_transactions(transactions=2, number_of_items=15)
    # print('Outliers created.')

    # generate some trends: 
    # i) over seasons

    # s_dates = {
    #    'y':[2022,2022], ->>>>>>['start', 'finish']
    #    'm':[5,8],
    #    'd':[1,30]
    #}
    # produce_transactions(transactions = 1,
    #                     seasonal_dates=s_dates)

    # s_dates = {
    #     'y':[2021,2021],
    #     'm':[5,8],
    #     'd':[1,30]
    # }
    # produce_transactions(transactions = 1,
    #                      seasonal_dates=s_dates)

    # s_dates = {
    #     'y':[2020,2020],
    #     'm':[5,8],
    #     'd':[1,30]
    # }
    # produce_transactions(transactions = 1,
    #                      seasonal_dates=s_dates)

    #s_dates = {
    #     'y':[2019,2019],
    #     'm':[5,8],
    #     'd':[1,30]
    # }
    # produce_transactions(transactions = 1,
    #                    seasonal_dates=s_dates)

    # ii) over customer segments (total cost and frequency)
    # -- over age 
    # date_of_birth = datetime(1993,2,2).date() # this is threshold.
    # iii) based on ratings of wine - DONE

