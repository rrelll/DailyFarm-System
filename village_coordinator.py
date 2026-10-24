from user import User

class VillageCoordinator(User):
    coordinator_counter = 1

    def __init__(self, username, password, email, contact=None):
        super().__init__(None, username, password, email)
        self._coordinatorId = f"VC{VillageCoordinator.coordinator_counter:03d}"
        VillageCoordinator.coordinator_counter += 1
        self._contactNumber = contact

    # Assign Driver 
    def assignDriver(self, driver_obj, delivery_id, price):
        # The VC sets the distance for the delivery to calculate the transport cost and to store for carbon emmission report
        distance = float(input(f"Enter distance for Delivery {delivery_id} (km): "))
        
        # Calculate Transport Cost for the payment report
        # business rule: RM0.80 per km to be relatable
        transport_cost = distance * 0.80 
        
        # We store the complete delivery data with price from the buyer's order
        delivery_data = {
            "id": delivery_id,
            "price": price,
            "distance": distance,
            "transport_cost": transport_cost,
            "status": "Assigned"
        }
        
        driver_obj.assigned_deliveries[delivery_id] = delivery_data
        print(f"[VC] Driver {driver_obj.get_username()} assigned to Delivery {delivery_id}")
        print(f"[VC] Order Price: RM{price:.2f} | Distance: {distance} km | Transport Cost: RM{transport_cost:.2f}")

    # Task 2: Confirm Delivery
    def confirmDelivery(self, driver_obj, delivery_id):
        if delivery_id in driver_obj.assigned_deliveries:
            # Just confirm/verify the delivery - Driver sets status to Delivered
            current_status = driver_obj.assigned_deliveries[delivery_id].get('status', 'Assigned')
            if current_status == "Delivered":
                driver_obj.assigned_deliveries[delivery_id]["status"] = "Confirmed by VC"
                print(f"[VC] Delivery {delivery_id} has been officially confirmed.")
            else:
                print(f"[VC] Error: Delivery {delivery_id} is not marked as Delivered yet.")
        else:
            print(f"[VC] Error: Delivery ID {delivery_id} not found for this driver.")

    # Task 3: Generate Payment Report
    def generatePaymentReport(self, driver_obj):
        print("\n" + "="*50)
        print(f"{'VILLAGE COORDINATOR FINANCIAL REPORT':^50}")
        print("="*50)
        
        # Fixed value from Case Study
        packing_fee = 3.00 
        # for the platform fee a rate is needed to calculate
        platform_fee_rate = 0.10 
        
        total_net_payout = 0
        report_data = []

        # Check the deliveries assigned to the specific driver
        if not driver_obj.assigned_deliveries:
            print("No completed deliveries to report.")
            return report_data

        for d_id, data in driver_obj.assigned_deliveries.items():
            gross_revenue = float(data['price'])
            transport_share = float(data['transport_cost']) # Based on Distance * 0.80(from the case study)
            platform_fee = gross_revenue * platform_fee_rate
            
            # the main formula from case study
            net_payout = gross_revenue - transport_share - packing_fee - platform_fee
            total_net_payout += net_payout

            # Store data for Officer to use
            report_data.append({
                "id": d_id,
                "net": net_payout,
                "transport": transport_share
            })

            print(f"Delivery ID: {d_id}")
            print(f"  > Gross Revenue:  RM{gross_revenue:.2f}")
            print(f"  > Transport Share: RM{transport_share:.2f}")
            print(f"  > Packing Fee:     RM{packing_fee:.2f}")
            print(f"  > Platform Fee:    RM{platform_fee:.2f}")
            print(f"  > NET PAYOUT:      RM{net_payout:.2f}")
            print("-" * 30)

        print(f"TOTAL PAYOUT TO FARMER: RM{total_net_payout:.2f}")
        print("="*50)
        
        return report_data

# Class VillageCoordinator Implemented by Eileen Ng Jing Jing (103918)