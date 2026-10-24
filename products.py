# Centralized product management system.
# Tracks all products added by farmers and makes them available for buyers.
class ProductManager:
    
    def __init__(self):
        self.products = {}  
    
    # Add a product for a farmer
    def add_product(self, farmer_id, product_name, price):
        if farmer_id not in self.products:
            self.products[farmer_id] = []
        
        # Check if product already exists
        for prod in self.products[farmer_id]:
            if prod["name"].lower() == product_name.lower():
                print(f"Product '{product_name}' already exists for this farmer.")
                return False
        
        self.products[farmer_id].append({
            "name": product_name,
            "price": float(price)
        })
        print(f"Product '{product_name}' added successfully for farmer {farmer_id}.")
        return True
    
    # Remove a product from a farmer's catalog
    def remove_product(self, farmer_id, product_name):
        if farmer_id not in self.products:
            print(f"No products found for farmer {farmer_id}.")
            return False
        
        original_count = len(self.products[farmer_id])
        self.products[farmer_id] = [
            p for p in self.products[farmer_id] 
            if p["name"].lower() != product_name.lower()
        ]
        
        if len(self.products[farmer_id]) < original_count:
            print(f"Product '{product_name}' removed successfully.")
            return True
        else:
            print(f"Product '{product_name}' not found.")
            return False
    
    # Update a product name and/or price for a farmer
    def update_product(self, farmer_id, old_product_name, new_product_name, new_price=None):
        if farmer_id not in self.products:
            print(f"No products found for farmer {farmer_id}.")
            return False
        
        for prod in self.products[farmer_id]:
            if prod["name"].lower() == old_product_name.lower():
                prod["name"] = new_product_name
                if new_price is not None:
                    prod["price"] = float(new_price)
                print(f"Product '{old_product_name}' updated to '{new_product_name}'.")
                return True
        
        print(f"Product '{old_product_name}' not found.")
        return False
    
    # Get all products for a specific farmer
    def get_farmer_products(self, farmer_id):
        return self.products.get(farmer_id, [])
    
    def get_all_products(self):
        """Get all available products from all farmers"""
        all_products = []
        for farmer_id, products in self.products.items():
            for product in products:
                all_products.append({
                    "farmer_id": farmer_id,
                    "name": product["name"],
                    "price": product["price"]
                })
        return all_products
    
    def get_product_by_name(self, product_name):
        """Find a product by name across all farmers"""
        for farmer_id, products in self.products.items():
            for product in products:
                if product["name"].lower() == product_name.lower():
                    return {
                        "farmer_id": farmer_id,
                        "name": product["name"],
                        "price": product["price"]
                    }
        return None
    
    # Display all available products
    def display_all_products(self):
        all_products = self.get_all_products()
        if not all_products:
            print("No products available at the moment.")
            return
        
        print("\n" + "="*50)
        print(f"{'AVAILABLE PRODUCTS':^50}")
        print("="*50)
        for idx, product in enumerate(all_products, 1):
            print(f"{idx}. {product['name']:20} | RM{product['price']:.2f} | Farmer: {product['farmer_id']}")
        print("="*50)


# Class Products Implemented by Theban A/L Vevindran (106554)