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
    salt = bcrypt.gensalt()
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'),salt)
    return hashed_pw

def generate_rand(mean,mode, prob_of_mode, sd=1, size = 1,precision=2):
    # a function that generates values based on a specified distribution.
    res = []
    for _ in range(size):
        if random.gauss(mu=0, sigma=sd)<=prob_of_mode:
            res.append(mode)
        else:
            res.append(abs(round(random.gauss(mu=mean,sigma=sd),precision)))
    return res

class Customer():
    def __init__(self, scene_id, first_name, last_name, password, full_address, city,postal_code, email, phone, credit_card, credit_card_expiry, store_credit, scene_points):
        self.scene_id = scene_id
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.full_address = full_address
        self.city = city
        self.postal_code = postal_code
        self.email = email
        self.phone = phone
        self.credit_card = credit_card
        self.credit_card_expiry = credit_card_expiry
        self.store_credit = store_credit
        self.scene_points = scene_points
    
    def __str__(self):
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


class ShoppingCart():

    def __init__(self, items, session_start_time, total_cost, customer_id):
        self.items = items
        self.session_start_time = session_start_time, 
        self.total_cost = total_cost
        self.customer_id = customer_id
        self.cart_id = uuid.uuid4()

    def  __str__(self):
        return f"""
        Cart_ID: {self.cart_id}
        Total Cart Items: {len(self.items)}
        Total Item Cost: {self.total_cost}
        Customer_ID: {self.customer_id}
        Cart Instantiated at: {self.session_start_time}
        """


if __name__ == '__main__':
# generate data that pertains to customers
    count = 1

    entries = 100
    customer_list = []
    for _ in range(entries):
        first_name = fake.first_name()
        last_name = fake.last_name()
        scene_ID = count
        password = hash_pw(fake.password())
        full_address = fake.address()
        city = fake.city()
        postal_code = fake.postalcode()
        email = str.lower(first_name) + '.' +str.lower(last_name) + '@' + fake.free_email_domain()
        phone = fake.phone_number()
        credit_card = fake.credit_card_full(card_type='mastercard')
        credit_card_expiry = fake.credit_card_expire()
        store_credit = generate_rand(mean=5, mode=0, prob_of_mode = 0.8, size = 1, precision = 2)[0]
        scene_points = generate_rand(mean=1000,mode=700,prob_of_mode=0.7,size=1)[0]
        customer = Customer(scene_ID, first_name, last_name, 
                            password, full_address, city, postal_code, 
                            email, phone, credit_card, credit_card_expiry, 
                            store_credit, scene_points)
        customer_list.append(customer)
        count += 1

    #products and suppliers
    wine_data = pd.read_csv('./wine_data/consolidated_wine_data.csv')

    # generate inventory for each product
    inventory = np.random.normal(loc=250, scale=3,size=len(wine_data))
    wine_data['inventory'] = inventory

    # generate data pertaining to transactions 
    # generate normal data across most of the products, 5% should have no sales.
    # generate random outliers
    # generate some trends: 
    # i) over seasons 
    # ii) over customer segments (total cost and frequency)
    # iii) based on ratings of wine

    # each transaction should contain the following:
    # 1) scene_id
    # 2) session_start_time
    # 3) session_end_time
    # 4) total_discount
    # 5) order_detail_id
    # 6) total_cost

    transactions = 1
    list_of_transactions = []

    def place_order( session_start_time,number_of_items=1,):
        pass
        cart = ShoppingCart(items=[],session_start_time = session_start_time,)
        for _ in range(number_of_items):
            # create purchasing bias towards higher rated wines
            if random.gauss(0,1) < 0.7:
                cart.items.append(wine_data[wine_data.rating>4.4].sample(1)) 


        wine_data

    def update_inventory():
        pass


    for transaction in range(transactions):
        date_time = fake.date_time_between(start_date = '-3y', end_date = 'now')
        # first choose random customer
        cust = np.random.choice(size = 1, a = customer_list)[0]
        session_start_time = date_time - timedelta(minutes = generate_rand(mean=4, mode=5, prob_of_mode = 0.5, sd = 2, precision = 0))
        total_discount = generate_rand(mean=5, mode = 2, prob_of_mode = 0.5, sd = 2, precision = 2)
        orders, order_detail_id = place_order()

