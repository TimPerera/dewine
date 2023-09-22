"""
shopping_cart.py
This module defines the ShoppingCart object which is used to containerize the Product objects
whilst a customer is shopping.
"""

from faker import Faker
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

from connection import Base

class ShoppingCart(Base):
    #  Generates a ShoppingCart which contains the shopped items. 
    __tablename__ = 'shoppingcart'

    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    products:Mapped[List["Product"]] = relationship(back_populates="shoppingcart")
    





















    def __init__(self, items):
        self.fake = Faker()
        self.items = items
        self.cart_id = self.fake.unique.random_int(min=1, max=999999)

    def __len__(self):
        return len(self.items)

    def  __str__(self):
        # What is called when a ShoppingCart object is called. 
        return f"""
        Cart_ID: {self.cart_id}
        Total Cart Items: {len(self.items)}
        """
    def __repr__(self):
        return f"<ShoppingCart CartID:{self.cart_id}. Total Cart Items: {len(self.items)}."

    def show_cart(self):
        for item in self.items:
            print(item)