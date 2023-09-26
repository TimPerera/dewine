"""
shopping_cart.py
This module defines the ShoppingCart object which is used to containerize the Product objects
whilst a customer is shopping.
"""
from typing import List
import logging

from faker import Faker
from sqlalchemy import ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from utils.logger import SetUpLogging
from config.connection import Base

SetUpLogging().setup_logging()


logger = logging.getLogger('dev')
logger.debug('path is Jello**********.')

#from .config import connection


association_table = Table("association_table",
                          Base.metadata,
                          Column("shoppingcart_id", ForeignKey("shoppingcart.id")),
                          Column("product_id",ForeignKey("product.id")))

class ShoppingCart(Base):
    #  Generates a ShoppingCart which contains the shopped items. 
    __tablename__ = 'shoppingcart'

    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    products:Mapped[List["Product"]] = relationship(secondary=association_table)
    transaction_id:Mapped[int] = mapped_column(ForeignKey("transactions.id"))
    transactions:Mapped["Transactions"] = relationship(back_populates="shoppingcart")

    def __init__(self, items):
        self.fake = Faker()
        self.products = items
        self.shoppingcart_id = self.fake.unique.random_int(min=1, max=999999)

    def __len__(self):
        return len(self.products)

    def  __str__(self):
        # What is called when a ShoppingCart object is called. 
        return f"""
        Cart_ID: {self.shoppingcart_id}
        Total Cart Items: {len(self.products)}
        """
    def __repr__(self):
        return f"<ShoppingCart CartID:{self.shoppingcart_id}. Total Cart Items: {len(self.products)}."

    def show_cart(self):
        for product in self.products:
            print(product)