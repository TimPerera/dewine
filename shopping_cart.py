from faker import Faker

class ShoppingCart():
    #  Generates a ShoppingCart option which contains the shopped items along with a time stamp. 
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
        Cart Instantiated at: {self.session_start_time}
        """