from typing import Optional
import pandas as pd

from sqlalchemy import ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from connection import Base
from utils import generate_rand

class Product(Base):
    __tablename__='product'

    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    #shoppingcart_id:Mapped[int] = mapped_column(ForeignKey("shoppingcart.id"))
    #shoppingcart:Mapped[Optional["ShoppingCart"]] = relationship(back_populates="products")
    #products:Mapped["ShoppingCart"] = relationship(secondary=association_table)
    wine_type:Mapped[str]
    name:Mapped[str]
    winery:Mapped[str] 
    country:Mapped[str]
    region:Mapped[str]
    quantity:Mapped[int]
    price:Mapped[int]
    year:Mapped[int]

    # Generates an instance of a product with all its details.
    def __init__(self):
        self.id = None
        self.wine_type = None
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
            self.wine_type = product.Type
            self.id = id
            self.name = product.Name
            self.winery = product.Winery
            self.region = product.Region
            self.rating = product.Rating
            self.price = product.Price
            self.year = product.Year
            self.country = product.Country
            self.inventory = generate_rand(mean=600, mode=550, prob_of_mode=0.5, sd=1.2, size=1,precision=0)[0]
        
        print('Products Loaded.')
        
    def __str__(self):
        return f'''
        Product ID: {self.id}
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
        print("Inventory updated")

