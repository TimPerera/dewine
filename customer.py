"""
customer.py
Provides functionality for Customer object. 
"""

import random
from typing import List
import datetime

from faker import Faker
import bcrypt
from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column

from utils import generate_rand
from shopping_cart import ShoppingCart
from connection import Base


class Customer(Base):
    # Generates an instance of a customer with all their details.
    __tablename__ = 'customer'

    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    first_name:Mapped[str] 
    last_name:Mapped[str]
    dob:Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True))
    password:Mapped[str]
    full_address:Mapped[str]
    city:Mapped[str]
    postal_code:Mapped[str]
    email:Mapped[str] = mapped_column(unique=True)
    phone:Mapped[str]
    credit_card:Mapped[str]
    credit_card_expiry:Mapped[str]
    store_credit:Mapped[float]
    scene_points:Mapped[float]
    # Ignore Pylint error below, string will be evaluated after all tables have been defined.
    transactions:Mapped[List["Transactions"]] = relationship(back_populates='customer')
    scene_plus:Mapped["ScenePlus"] = relationship(back_populates="customer")

    def __init__(self):
        self.fake = Faker()
        self.first_name = self.fake.first_name()
        self.last_name = self.fake.last_name()
        self.full_name = self.first_name + self.last_name
        self.dob = self.fake.date_of_birth(minimum_age = 18, maximum_age=90)
        self.scene_ID = self.fake.unique.random_int(min=1, max=999999)
        self.password = self.hash_pw(self.fake.password())
        self.full_address = self.fake.address()
        self.city = self.fake.city()
        self.postal_code = self.fake.postalcode()
        self.email = str.lower(self.first_name) + '.' +str.lower(self.last_name) + '@' + self.fake.free_email_domain()
        self.phone = self.fake.phone_number()
        self.credit_card = self.fake.credit_card_full(card_type='mastercard')
        self.credit_card_expiry = self.fake.credit_card_expire()
        self.store_credit = generate_rand(mean=5, mode=0, prob_of_mode = 0.8, size = 1, precision = 2)[0]
        self.scene_points = generate_rand(mean=1000,mode=700,prob_of_mode=0.55,size=1)[0]
    
    def hash_pw(self,password):
        # secures password via salting
        salt = bcrypt.gensalt()
        hashed_pw = bcrypt.hashpw(password.encode('utf-8'),salt)
        return hashed_pw

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
