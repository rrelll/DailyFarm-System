from farmer import Farmer
from driver import Driver
from buyer import Buyer
from officer import Officer
from village_coordinator import VillageCoordinator
from products import ProductManager

# Pre-registered users list
all_users = []  # Initialize empty list to store all users

# Initialize ProductManager for centralized product management
product_manager = ProductManager()


# Pre-registered users (Later can use this for login)
pre_registered = [
    Farmer("John Cena", "Cena123", "jcena@gmail.com"),
    Driver("Marc", "Marc123", "marc@gmail.com", "08123456789"),
    Buyer("Roman Reigns", "Roman123", "roman@gmail.com", "123 Farm Road", "0123456789"),
    Officer("Naoi Rei", "Rei456", "rei@gmail.com"),
    VillageCoordinator("Pak Joko", "Joko123", "joko@gmail.com")
]

# Add pre-registered users to the main user list
all_users.extend(pre_registered)


# Global list of pending deliveries (buyers place orders here)
pending_deliveries = []

# Global delivery counter for simple sequential IDs
delivery_counter = 1

# Menu for the program ( Main loop )
while True:
    print("\n1. Register\n2. Login\n3. Exit")
    choice = input("Choose an option: ")

    # Register
    if choice == "1":
        print("--- Registration ---")
        role = input("Enter role (Farmer/Driver/Buyer/Officer/Village Coordinator): ").strip().lower()
        username = input("Enter username: ")
        password = input("Enter password: ")
        email = input("Enter email: ")

        if role == "farmer":
            new_user = Farmer(username, password, email)
        elif role == "driver":
            contact = input("Enter Driver Contact Number: ").strip()
            while not contact:
                print("Contact number is required for drivers.")
                contact = input("Enter Driver Contact Number: ").strip()
            new_user = Driver(username, password, email, contact)
        elif role == "buyer":
            # Capturing required fields for the Buyer class
            address = input("Enter delivery address: ")
            contact = input("Enter contact number: ")
            new_user = Buyer(username, password, email, address, contact)
        elif role == "officer":
            new_user = Officer(username, password, email)
        elif role == "village coordinator":
            new_user = VillageCoordinator(username, password, email)
        else:
            print("Invalid role! Registration failed.")
            continue

        all_users.append(new_user)
        print(f"'{username}' Registered successfully! Your User ID: {new_user._userId}")

    # Login
    elif choice == "2":
        print("--- Login ---")
        role = input("Enter role (Farmer/Driver/Buyer/Officer/Village Coordinator): ").strip().lower()
        username = input("Enter username: ")
        password = input("Enter password: ")

        logged_in = False
        for user in all_users:
            if ((role == "farmer" and isinstance(user, Farmer)) or
                (role == "driver" and isinstance(user, Driver)) or
                (role == "buyer" and isinstance(user, Buyer)) or
                (role == "officer" and isinstance(user, Officer)) or
                (role == "village coordinator" and isinstance(user, VillageCoordinator))):
                if user.login(username, password):
                    print(f"Login successful! Welcome, {username}")
                    user.displayDashboard()
                    if isinstance(user, Farmer):
                        while True:
                            print("\n--- Farmer Dashboard ---")
                            print("1. Add Product")
                            print("2. Update Product")
                            print("3. View My Products")
                            print("4. Logout")
                            dash_choice = input("Choose an option: ")
                            if dash_choice == "1":
                                product = input("Enter product name: ")
                                price = input("Enter product price (RM): ")
                                product_manager.add_product(user._farmerId, product, price)
                            elif dash_choice == "2":
                                old = input("Enter product name to update: ")
                                new = input("Enter new product name: ")
                                new_price = input("Enter new price (RM) (or press Enter to keep same): ")
                                if new_price.strip():
                                    product_manager.update_product(user._farmerId, old, new, new_price)
                                else:
                                    product_manager.update_product(user._farmerId, old, new)
                            elif dash_choice == "3":
                                products = product_manager.get_farmer_products(user._farmerId)
                                if products:
                                    print(f"\n--- Products of Farmer {user._farmerId} ---")
                                    for prod in products:
                                        print(f"- {prod['name']}: RM{prod['price']:.2f}")
                                else:
                                    print("You have not added any products yet.")
                            elif dash_choice == "4":
                                print("Logging out...")
                                break
                            else:
                                print("Invalid option.")
                    elif isinstance(user, Buyer):
                        while True:
                            print("\n--- Buyer Dashboard ---")
                            print("1. Place Order & Make Payment")
                            print("2. View My Statement")
                            print("3. Logout")
                            
                            dash_choice = input("Choose an option: ")

                            if dash_choice == "1":
                                # Show all available products
                                all_products = product_manager.get_all_products()
                                
                                if not all_products:
                                    print("No products available at the moment.")
                                    continue
                                
                                product_manager.display_all_products()
                                
                                # to let buyesr select a product
                                try:
                                    product_choice = int(input("Enter product number to order (or 0 to cancel): "))
                                    if product_choice == 0:
                                        continue
                                    if product_choice < 1 or product_choice > len(all_products):
                                        print("Invalid product number.")
                                        continue
                                    
                                    selected = all_products[product_choice - 1]
                                    item = selected["name"]
                                    price = selected["price"]
                                    
                                    print(f"\nOrdering {item} for RM{price:.2f}")
                                    
                                    delivery_id = f"DEL{delivery_counter:03d}"
                                    
                                    # placeOrder handles internal payment and returns delivery details including price
                                    order_data = user.placeOrder(item, price, delivery_id)
                                    
                                    if order_data and order_data[0]:
                                        # Store complete order data (delivery_id, address, price) for Village Coordinator
                                        pending_deliveries.append({
                                            "delivery_id": order_data[0],
                                            "address": order_data[1],
                                            "price": float(order_data[2])
                                        })
                                        delivery_counter += 1
                                        print("Order placed! Status: Waiting for Coordinator to assign a driver.")
                                except ValueError:
                                    print("Please enter a valid number.")
                                    
                            elif dash_choice == "2":
                                # Calls the public method that accesses the private statement
                                user.displayStatement()
                                
                            elif dash_choice == "3":
                                print("Logging out...")
                                break
                            else:
                                print("Invalid option.")

                    elif isinstance(user, Driver):
                        while True:
                            print("\n--- Driver Dashboard ---")
                            print("1. My Deliveries")
                            print("2. Update Delivery Status")
                            print("3. Update My Availability")
                            print("4. Logout")
                            
                            choice = input("\nChoose an option: ")

                            if choice == "1":
                                user.viewAssignedDeliveries()
                            
                            elif choice == "2":
                                did = input("Enter Delivery ID : ")
                                print("Status options: Pending, In Transit, Delivered")
                                new_stat = input("Enter new status: ")
                                user.updateDeliveryStatus(did, new_stat)
                                
                            elif choice == "3":
                                print("Status options: Available, Busy, On Break")
                                new_stat = input("Enter new status: ")
                                user.updateAvailability(new_stat)
                                
                            elif choice == "4":
                                print("Logging out...")
                                break
                            else:
                                print("Invalid selection.")
                    elif isinstance(user, VillageCoordinator):
                        while True:
                            print("\n--- Village Coordinator Dashboard ---")
                            print("1. Assign Driver")
                            print("2. Confirm Delivery")
                            print("3. Generate Payment Report")
                            print("4. Exit")

                            choice = input("Choose an option: ")

                            if choice == "1":
                                delivery_id = input("Enter Delivery ID: ")
                                driver_username = input("Enter Driver Username: ")
                                
                                # to find the order price from pending_deliveries
                                order_price = None
                                for order in pending_deliveries:
                                    if order["delivery_id"] == delivery_id:
                                        order_price = order["price"]
                                        break
                                
                                if order_price is None:
                                    print(f"Error: Delivery ID {delivery_id} not found in pending orders.")
                                    continue
                                
                                # to find the driver in all_users
                                driver_found = False
                                for person in all_users:
                                    if isinstance(person, Driver) and person.get_username() == driver_username:
                                        user.assignDriver(person, delivery_id, order_price)
                                        driver_found = True
                                        break
                                if not driver_found:
                                    print(f"Error: Driver '{driver_username}' not found.")

                            elif choice == "2":
                                delivery_id = input("Enter Delivery ID: ")
                                driver_username = input("Enter Driver Username: ")
                                
                                # to find the driver in all_users
                                driver_found = False
                                for person in all_users:
                                    if isinstance(person, Driver) and person.get_username() == driver_username:
                                        user.confirmDelivery(person, delivery_id)
                                        driver_found = True
                                        break
                                if not driver_found:
                                    print(f"Error: Driver '{driver_username}' not found.")

                            elif choice == "3":
                                driver_username = input("Enter Driver Username: ")
                                
                                # to find the driver in all_users
                                driver_found = False
                                for person in all_users:
                                    if isinstance(person, Driver) and person.get_username() == driver_username:
                                        user.generatePaymentReport(person)
                                        driver_found = True
                                        break
                                if not driver_found:
                                    print(f"Error: Driver '{driver_username}' not found.")

                            elif choice == "4":
                                print("Logging out...")
                                break
                            else:
                                print("Invalid option. Try again.")

                    elif isinstance(user, Officer):
                        while True:
                            print("\n--- Officer Dashboard ---")
                            print("1. Generate Carbon Emission Report")
                            print("2. View Payment Report")
                            print("3. View Order Status")
                            print("4. Logout")
                            
                            choice = input("Choose an option: ")

                            if choice == "1":
                                # Finding the Driver to access distance data set by VC
                                target_driver = next((u for u in all_users if isinstance(u, Driver)), None)
                                if target_driver:
                                    user.generateCarbonEmissionReport(target_driver.assigned_deliveries)
                                else:
                                    print("Error: No driver data found in system.")

                            elif choice == "2":
                                # getting the payout data from the VC to report
                                target_vc = next((u for u in all_users if isinstance(u, VillageCoordinator)), None)
                                target_driver = next((u for u in all_users if isinstance(u, Driver)), None)
                                
                                if target_vc and target_driver:
                                    # Officer views the report generated by the VC
                                    report = target_vc.generatePaymentReport(target_driver)
                                    user.viewPaymentReport(report)
                                else:
                                    print("Error: Financial data unavailable.")

                            elif choice == "3":
                                # Officer checks orders waiting for VC action
                                user.viewOrderStatus(pending_deliveries)

                            elif choice == "4":
                                print("Logging out...")
                                break
                            else:
                                print("Invalid option.")

                    logged_in = True
                    break
        if not logged_in:
            print("Invalid username, password, or role. Try again or register.")

    # Exit
    elif choice == "3":
        print("Exiting...")
        break
    else:
        print("Invalid option. Try again.")


# ===================================================
# Main program implemented and updated by 
# 1. Darryl Anak Staban Lanjang (103794)
# 2. Theban A/L Vevindran (106554)
# 3. Salwen Ernest Empas (100926) 
# 4. Muhammad Syafrul Hadzim Bin Mohamad Azlan (99983) 
# 5. Eileen Ng Jing Jing (103918)
# ===================================================
