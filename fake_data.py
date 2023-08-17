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

    def __init__(self, items, session_start_time):
        self.items = items
        self.session_start_time = session_start_time, 
        self.cart_id = uuid.uuid4()

    def  __str__(self):
        return f"""
        Cart_ID: {self.cart_id}
        Total Cart Items: {len(self.items)}
        Cart Instantiated at: {self.session_start_time}
        """


if __name__ == '__main__':
# generate data that pertains to customers
    count = 1

    entries = 5
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

    # generate data pertaining to transactions - DONE
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

    transactions = 10
    list_of_transactions = []

    def get_items(session_start_time,number_of_items=1,):
        cart = ShoppingCart(items=[],session_start_time = session_start_time)
        # items = {product_name : quantity}
        for _ in range(number_of_items):
            # create purchasing bias towards higher rated wines
            if random.gauss(0,1) < 0.7:
                product_idx  = wine_data.Name[wine_data.Rating>4.4].sample(1).index[0]
            else:
                product_idx  = wine_data.Name.sample(1).index[0]
            quantity = generate_rand(mean = 2, mode = 1,prob_of_mode = 0.8,size = 1,precision = 0)[0]

            product = {
                'product_idx': product_idx,
                'product_name' : wine_data.iloc[product_idx].Name,
                'product_winery' : wine_data.iloc[product_idx].Winery,
                'product_country' : wine_data.iloc[product_idx].Country,
                'product_region' : wine_data.iloc[product_idx].Region,
                'product_quantity' : quantity,
                'product_price' : wine_data.iloc[product_idx].Price
            }
            cart.items.append(product)
        update_inventory(cart.items)
        transaction_id = fake.unique.random_int(min=111111, max=999999)
        return cart, transaction_id

    def update_inventory(cart):
        # Updates inventory, negative values represent pre-orders for once stocks become available.
        # TODO: Make SQL call to update inventory table
        for product in cart:
            wine_data.loc[product.get('product_idx'),'inventory'] -= product.get('product_quantity')
            if wine_data.iloc[product.get('product_idx')].inventory <= 5: 
                print(f"Warning Low Inventory for {product.get('product_idx')}: {product.get('product_name')}")
            #print(f"Inventory Updated for {product.get('product_idx')}: {product.get('product_name')}")

    def produce_transactions(transactions, number_of_items=False):
    # create transaction using place_order method, update inventory straight after.
        for transaction in range(transactions): # One transaction per customer
            if not number_of_items: int(generate_rand(mean = 3, mode = 2, prob_of_mode=0.5, sd=2, precision=0)[0])
            date_time = fake.date_time_between(start_date = '-3y', end_date = 'now')
            # first choose random customer
            cust = np.random.choice(size = 1, a = customer_list)[0] # test to see if repeat customers are observed
            session_start_time = date_time #- timedelta(minutes = generate_rand(mean=4, mode=5, prob_of_mode = 0.5, sd = 2, precision = 0))
            total_discount = generate_rand(mean=5, mode = 2, prob_of_mode = 0.5, sd = 2, precision = 2)
            cart, order_detail_id = get_items(date_time, number_of_items = generate_rand(mean = 3, mode = 2, prob_of_mode=0.5, sd=2, precision=0)[0])
            total_price = 0
            for product in cart.items:
                total_price += round(product.get('product_price') * product.get('product_quantity'),2)
            total_quantity = 0

            print(f'''
            Transaction Details:
            Date/Time: {date_time}
            Customer: {cust.first_name + ' ' + cust.last_name}
            Order ID: {order_detail_id}
            Products: {[product.get('product_name') for product in cart.items] }
            Quantity: {round(sum([product.get('product_quantity') for product in cart.items]),0)}
            Total Cost: ${total_price}
            ''')
    
    # generate data pertaining to transactions - DONE
    produce_transactions(transactions = 10)
    # generate normal data across most of the products, 5% should have no sales.
    # generate random `number_of_items` outliers
    print("******** Outliers")
    [produce_transactions(transactions=5,number_of_items = x) for x in generate_rand(mean=40,mode=35,prob_of_mode=0.7,sd=4,size=5)]
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
    

    

