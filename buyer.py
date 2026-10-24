from user import User

class Buyer(User):
    buyer_counter = 1
    
    def __init__(self, username, password, email, address=None, contact=None):
        # Passes login info to User superclass
        super().__init__(None, username, password, email)
        
        self.__buyerID = f"B{Buyer.buyer_counter:03d}"
        self.__buyerName = username
        self.__address = address
        self.__contactNumber = contact
        
        Buyer.buyer_counter += 1

    # PlaceOrder()
    def placeOrder(self, product_name, price, delivery_id):
        print(f"\n--- Initiating Order for {product_name} ---")
        
        # placeOrder triggers the payment process
        if self.__makePayment(price):
            print(f"Order Successful! Delivery ID {delivery_id} created.")
            return delivery_id, self.__address, price
        return None, None, None

    # makePayment()
    def __makePayment(self, amount):
        print(f"Processing payment of RM{amount}...")
        print("Payment Confirmed via Secure Gateway.")
        return True

    # viewStatement() 
    def __viewStatement(self):
        print(f"\n--- Digital Statement for {self.__buyerName} ---")
        print(f"Account ID: {self.__buyerID}")
        print("Status: All recent payments cleared.")

    # Public helper to access the private statement method
    def displayStatement(self):
        self.__viewStatement()
        
    # Getter for Address (used when creating a Delivery object)
    def getAddress(self):
        return self.__address


# Class Buyer Implemented by Salwen Ernest Empas  (100926)