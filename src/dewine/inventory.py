"""
`inventory.py`
This module defines the Inventory class. This class is needed as a placeholder
for all products and their respective available quantities, and updates these 
quantities when customer purchases are made.
"""
import pandas as pd
import logging

from utils.utils import generate_rand
from dewine.product import Product
from utils.logger import SetUpLogging

SetUpLogging().setup_logging()
logger = logging.getLogger('dev')

class Inventory():
    def __init__(self, data_path):
        # Upon initialization loads data 
        data = pd.read_csv(data_path)
        self.items = self.populate_inventory(data)

    def update_inventory(self, cart, direction = 'negative'):
        # Updates inventory, negative values represent pre-orders for once stocks become available.
        # TODO: Make SQL call to update inventory table
        for product in cart:
            if direction == 'negative':
                product.inventory -= product.quantity # remove ordered items from inventory
                if product.inventory <= 5: 
                    logger.warning(f"Warning Low Inventory for {product.idx}: {product.name}")
            else:
                product.inventory -= product.quantity
        logger.debug("Inventory updated for {}".format([product.name for product in cart]))

    def populate_inventory(self, data):
        # Generate product info
        product_list = []
        for id, data in enumerate(data.itertuples()):
            product = Product()
            product.wine_type = data.Type
            product.idx = id
            product.name = data.Name
            product.winery = data.Winery
            product.region = data.Region
            product.country = data.Country
            product.rating = data.Rating
            product.price = data.Price
            product.year = data.Year
            product.inventory = generate_rand(mean=600, mode=550, prob_of_mode=0.5, sd=1.2, size=1,precision=0)[0]
            product_list.append(product)
        logger.info('Database uploaded.')
        return product_list