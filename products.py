from utils import generate_rand

class Product():
    # Generates an instance of a product with all its details.
    def __init__(self):
        self.idx = None
        self.type = None
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
            self.type = product.Type
            self.idx = id
            self.name = product.Name
            self.winery = product.Winery
            self.region = product.Region
            self.rating = product.Rating
            self.price = product.Price
            self.year = product.Year
            self.inventory = generate_rand(mean=600, mode=550, prob_of_mode=0.5, sd=1.2, size=1,precision=0)[0]
        print('Products Loaded.')
        
    
    def __str__(self):
        return f'''
        Product ID: {self.idx}
        Product Name: {self.name}
        Product Winery: {self.winery}
        Product Year: {self.year}
        Product Price: {self.price}
        '''