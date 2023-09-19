import pandas as pd

from sqlalchemy import Column, String, Float, Integer
from sqlalchemy.ext.declarative import declarative_base

from products import Product
from utils import generate_rand

Base = declarative_base()

class Inventory(Base):
    __tablename__ = 'inventory'

    product_id = Column(Integer, primary_key=True)
    product_type = Column(String)
    product_idx = Column(Integer)
    product_name = Column(String)
    product_winery = Column(String)
    product_region = Column(String)
    product_rating = Column(Float)
    product_price = Column(Float)
    product_year = Column(Integer)
    product_quantity = Column(Integer)

    def __init__(self, data_path):
        # Upon initialization loads data 
        data = pd.read_csv(data_path)
        self.product = Product()
        self.product.type = None
        self.product.idx = None
        self.product.name = None
        self.product.winery = None
        self.product.region = None
        self.product.rating = None
        self.product.price = None
        self.product.year = None
        self.product.inventory = None
        self.list = self.populate_inventory(data)

    def update_inventory(self, cart):
        # Updates inventory, negative values represent pre-orders for once stocks become available.
        # TODO: Make SQL call to update inventory table
        for product in cart:
            product.inventory -= product.quantity # remove ordered items from inventory
            if product.inventory <= 5: 
                print(f"Warning Low Inventory for {product.idx}: {product.name}")
        print("Inventory updated")

    def populate_inventory(self, wine_data):
        # Generate product info
        product_list = []
        for id, data in enumerate(wine_data.itertuples()):
            self.product = Product()
            self.product.type = data.Type
            self.product.idx = id
            self.product.name = data.Name
            self.product.winery = data.Winery
            self.product.region = data.Region
            self.product.rating = data.Rating
            self.product.price = data.Price
            self.product.year = data.Year
            self.product.inventory = generate_rand(mean=600, mode=550, prob_of_mode=0.5, sd=1.2, size=1,precision=0)[0]
            product_list.append(product)
        print('Database uploaded.')
        return product_list
