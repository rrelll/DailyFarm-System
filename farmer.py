from user import User

# Subclass: Farmer (Inheritance from User Class)
class Farmer(User):
    farmer_counter = 1 # Class variable to auto-generate farmer ID

    def __init__(self, username, password, email):
        super().__init__(None, username, password, email)
        self._farmerId = f"F{Farmer.farmer_counter:03d}"
        Farmer.farmer_counter += 1
        self.products = []  # initialize empty list to store the products later


    def addProduct(self, product):      
        self.products.append(product)
        print(f"Product '{product}' added successfully.")


    def updateProduct(self, old_product, new_product):
        if old_product in self.products:
            index = self.products.index(old_product)
            self.products[index] = new_product
            print(f"Product '{old_product}' updated to '{new_product}'.")
        else:
            print(f"Product '{old_product}' not found.")


    def viewProducts(self):
        print(f"Products of Farmer ID {self._farmerId}:")
        for product in self.products:
            print(f"- {product}")

# Class Farmer Implemented by Darryl Anak Staban Lanjang (103794)