from dateutil.relativedelta import relativedelta
from faker import Faker
from datetime import datetime

class Transaction():

    def __init__(self, customer, cart, time_limits, discount=0):
        self.fake = Faker()
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
        session_start_time = self.fake.date_time_between(start_date = start_date, end_date = end_date)
        return session_start_time

    def generate_transaction_id(self):
        transaction_id = self.fake.unique.random_int(min=111111, max=999999)
        return transaction_id

    def get_total(self):
        total_price = 0
        for product in self.cart.items:
            total_price += product.price * product.quantity 
        total_price = round(total_price,2)
        return total_price
    
    def get_discount(self, discount):
        return discount*self.get_total()