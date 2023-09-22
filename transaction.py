from dateutil.relativedelta import relativedelta
from faker import Faker
import datetime

from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase

from connection import Base

class Transactions(Base):
    __tablename__ = 'transactions'
    
    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    discount:Mapped[float]
    cart_id:Mapped[int] = mapped_column(ForeignKey('cart.id'))
    session_time:Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    discount_total:Mapped[float]
    total_cost:Mapped[float]
    customer_id:Mapped[int] = mapped_column(ForeignKey('customer.id'))
    customer:Mapped["Customer"] = relationship(back_populates='transactions')
   
    fake = Faker()
    def __init__(self, customer, cart, time_limits, discount=0):
        print('INITIALIZED TRANSACTIONS')
        self.id = self.generate_transaction_id()
        self.fake = Faker()
        self.discount = discount
        self.customer = customer
        self.cart = cart
        self.session_time = self.generate_session_time(time_limits)
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

