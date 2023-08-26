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
    def __init__(self, items, session_start_time):
        self.items = items
        self.session_start_time = session_start_time, 
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

    def get_items(self, products, session_start_time,number_of_items=1, bias=True, type= None):
        # Fetches a product along with all its details. This method replicates the action of a customer selecting products (with varying quantities)
        # create purchasing bias towards higher rated wines
        
        cart = ShoppingCart(items=[],session_start_time = session_start_time)
        high_rated_products = low_rated_products = []
        if type:
            high_rated_products = [product for product in products if product.rating > 4.4 and product.type == type]
            low_rated_products = [product for product in products if product.rating <= 4.4 and product.type == type]
        else:
            high_rated_products = [product for product in products if product.rating > 4.4]
            low_rated_products = [product for product in products if product.rating <= 4.4]
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
        transaction_id = fake.unique.random_int(min=111111, max=999999)
        return cart, transaction_id
        
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
def update_inventory(cart):
    # Updates inventory, negative values represent pre-orders for once stocks become available.
    # TODO: Make SQL call to update inventory table
    for product in cart:
        product.inventory -= product.quantity # remove ordered items from inventory
        if product.inventory <= 5: 
            print(f"Warning Low Inventory for {product.idx}: {product.name}")

### -----------------------------------------------------------
### Create Data
### -----------------------------------------------------------
# generate data that pertains to customers
entries = 5 # number of customers to generate
customer_list = [Customer() for _ in range(entries)]
# Load products and suppliers
wine_data = pd.read_csv('./wine_data/consolidated_wine_data.csv')
product_list = []
transactions = 10
list_of_transactions = []

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

def produce_transactions(transactions, number_of_items=False, seasonal_dates = None, type = None, less_than_age_condition = None, greater_than_age_condition = None):
    # create transaction, update inventory straight after.
    # each transaction should contain the following:
    # 1) scene_id
    # 2) session_start_time
    # 3) session_end_time
    # 4) total_discount
    # 5) order_detail_id
    # 6) total_cost
    
    # for each year till end year - set year
    # for each month till end month - set month       
    # for each day till end day - set date
    for _ in range(transactions): # One transaction per customer
        if not number_of_items: 
            number_of_items = generate_rand(mean = 3, mode = 2, prob_of_mode=0.5, sd=1, precision=0)[0]
        # ability to introduce seasonality in data.
        if seasonal_dates:
            start_date = datetime(seasonal_dates['y'][0],seasonal_dates['m'][0],seasonal_dates['d'][0])
            end_date = datetime(seasonal_dates['y'][1],seasonal_dates['m'][1],seasonal_dates['d'][1])
            session_start_time = fake.date_time_between(start_date = start_date, end_date = end_date)
        else:
            session_start_time = fake.date_time_between(start_date = '-3y', end_date = 'now')
        # first choose random customer, with ability to discriminate across ages
        if less_than_age_condition:
            eligible = [cust for cust in customer_list if cust.dob >= less_than_age_condition]
        elif greater_than_age_condition:
            eligible = [cust for cust in customer_list if cust.dob <= greater_than_age_condition]

        if not eligible:
            customer = np.random.choice(size = 1, a = customer_list)[0]
        elif len(eligible)==1:
            customer = eligible[0]
        else:
            customer = random.sample(eligible, 1)[0]
        #total_discount = generate_rand(mean=5, mode = 2, prob_of_mode = 0.5, sd = 2, precision = 2)
        cart, order_detail_id = customer.get_items(product_list, session_start_time, number_of_items = number_of_items, type = type)
        update_inventory(cart.items)
        total_price = 0
        for product in cart.items:
            total_price += product.price * product.quantity 
        total_price = round(total_price,2)
        print(f'''
        Transaction Details:
        Date/Time: {session_start_time}
        Customer: {customer.first_name + ' ' + customer.last_name}
        Customer Age: {relativedelta(datetime.now().date(), customer.dob).years}
        Order ID: {order_detail_id}
        Products: {[product.name for product in cart.items] }
        Quantity: {sum([product.quantity for product in cart.items])}
        Total Cost: ${total_price}
        ''')

# generate data pertaining to transactions - DONE
#produce_transactions(transactions = 5)
#print('Complete!')
# generate normal data across most of the products, 5% should have no sales.
# generate random `number_of_items` outliers
#produce_transactions(transactions=2, number_of_items=15)
#print('Outliers created.')

# generate some trends: 
# i) over seasons

#s_dates = {
#    'y':[2022,2022],
#    'm':[5,8],
#    'd':[1,30]
#}
#produce_transactions(transactions = 1,
#                     seasonal_dates=s_dates)

#s_dates = {
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
#produce_transactions(transactions = 1,
#                    seasonal_dates=s_dates)

# ii) over customer segments (total cost and frequency)
# -- over age 
date_of_birth = datetime(1993,2,2).date()
produce_transactions(transactions=1,
                     greater_than_age_condition = date_of_birth)
# iii) based on ratings of wine - DONE

