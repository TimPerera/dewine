import pandas as pd
from products import Product
from utils import generate_rand

class Inventory():
    def __init__(self, data_path):
        # Upon initialization loads data 
        data = pd.read_csv(data_path)
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
            product = Product()
            product.type = data.Type
            product.idx = id
            product.name = data.Name
            product.winery = data.Winery
            product.region = data.Region
            product.rating = data.Rating
            product.price = data.Price
            product.year = data.Year
            product.inventory = generate_rand(mean=600, mode=550, prob_of_mode=0.5, sd=1.2, size=1,precision=0)[0]
            product_list.append(product)
        print('Database uploaded.')
        return product_list
