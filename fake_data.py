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
from faker import Faker
import bcrypt
import random
import numpy as np
import pandas as pd
import uuid
# customer
fake = Faker()

def hash_pw(password):
    # secures password via salting
    salt = bcrypt.gensalt()
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'),salt)
    return hashed_pw

def generate_rand(mean,mode, prob_of_mode, sd=1, size = 1,precision=2):
    # a function that generates values based on a specified distribution.
    # value returned will always be positive.
    res = []
    for _ in range(size):
        if random.random()<=prob_of_mode:
            if precision ==0:
                res.append(int(abs(round(mode,precision))))
            else:
                res.append(abs(round(mode,precision)))
        else:
            if precision == 0:
                res.append(int(abs(round(random.gauss(mu=mean,sigma=sd),precision))))
            else:
                res.append(abs(round(random.gauss(mu=mean,sigma=sd),precision)))
    return res

class ShoppingCart():
    #  Generates a ShoppingCart option which contains the shopped items along with a time stamp. 
    def __init__(self, items, session_start_time):
        self.items = items
        self.session_start_time = session_start_time, 
        self.cart_id = uuid.uuid4()

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
        self.name = None
        self.winery = None
        self.country = None
        self.region = None
        self.quantity = None
        self.price = None
        self.year = None
        self.inventory = None

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
        
    def update_inventory(self, cart):
        # Updates inventory, negative values represent pre-orders for once stocks become available.
        # TODO: Make SQL call to update inventory table
        for product in cart:
            product.inventory -= product.quantity # remove ordered items from inventory
            if product.inventory <= 5: 
                print(f"Warning Low Inventory for {product.idx}: {product.name}")
    

class Customer():
    # Generates an instance of a customer with all their details. 
    def __init__(self):

        self.first_name = fake.first_name()
        self.last_name = fake.last_name()
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

    def get_items(self, products, session_start_time,number_of_items=1, bias=True):
        # Fetches a product along with all its details. This method replicates the action of a customer selecting products (with varying quantities)
        # create purchasing bias towards higher rated wines
        cart = ShoppingCart(items=[],session_start_time = session_start_time)
        high_rated_products = [product for product in products if product.rating > 4.4]
        low_rated_products = [product for product in products if product.rating <= 4.4]
        threshold =  0.7 if bias else 0.5 
        for _ in range(number_of_items):
            if random.gauss(0,1) < threshold:
                products_selected  = random.choice(high_rated_products)
            else:
                products_selected  = random.choice(low_rated_products)
        cart.items += products_selected
        transaction_id = fake.unique.random_int(min=111111, max=999999)
        return cart, transaction_id
        
    def __str__(self):
        # What is printed out when a customer instance is called. 
        return f''' 
        Customer SceneID = {self.scene_id}
        Name: {" ".join([self.first_name, self.last_name])}
        Address: {self.full_address}
        Email: {self.email}
        Phone: {self.phone}
        Payment Method Available: {self.credit_card is not None}
        Store Credit: ${self.store_credit}
        Scene Points: {self.scene_points}
        '''


### -----------------------------------------------------------
### Create Data
### -----------------------------------------------------------
# generate data that pertains to customers
entries = 5 # number of customers to generate
customer_list = [Customer() for _ in entries]
# Load products and suppliers
wine_data = pd.read_csv('./wine_data/consolidated_wine_data.csv')
# generate inventory for each product
inventory = np.random.normal(loc=250, scale=3,size=len(wine_data))
wine_data['inventory'] = inventory
transactions = 10
list_of_transactions = []

def produce_transactions(transactions, number_of_items=False):
# create transaction using place_order method, update inventory straight after.
    # each transaction should contain the following:
    # 1) scene_id
    # 2) session_start_time
    # 3) session_end_time
    # 4) total_discount
    # 5) order_detail_id
    # 6) total_cost    
    products = Product()
    products.load_products(wine_data)

    for _ in range(transactions): # One transaction per customer
        if not number_of_items: int(generate_rand(mean = 3, mode = 2, prob_of_mode=0.5, sd=2, precision=0)[0])
        print('number of items')
        session_start_time = fake.date_time_between(start_date = '-3y', end_date = 'now')
        # first choose random customer
        customer = np.random.choice(size = 1, a = customer_list)[0] # test to see if repeat customers are observed
        #- timedelta(minutes = generate_rand(mean=4, mode=5, prob_of_mode = 0.5, sd = 2, precision = 0))
        total_discount = generate_rand(mean=5, mode = 2, prob_of_mode = 0.5, sd = 2, precision = 2)
        cart, order_detail_id = customer.get_items(products, session_start_time, number_of_items = number_of_items)
        products.update_inventory(cart)
        total_price = 0
        for product in cart.items:
            total_price += product.price * product.quantity
        total_price = round(total_price,2)
        
        print(f'''
        Transaction Details:
        Date/Time: {session_start_time}
        Customer: {customer.first_name + ' ' + customer.last_name}
        Order ID: {order_detail_id}
        Products: {[product.get('product_name') for product in cart.items] }
        Quantity: {sum([product.get('product_quantity') for product in cart.items])}
        Total Cost: ${total_price}
        ''')

# generate data pertaining to transactions - DONE
produce_transactions(transactions = 140)
# generate normal data across most of the products, 5% should have no sales.
# generate random `number_of_items` outliers
[produce_transactions(transactions=5,number_of_items = x) for x in generate_rand(mean=15,mode=12,prob_of_mode=0.7,sd=2,size=5, precision=0) if x >= 1]

# generate some trends: 
# i) over seasons 
# ii) over customer segments (total cost and frequency)
# iii) based on ratings of wine


    

