from user import User

class Officer(User):
    off_counter = 1

    def __init__(self, username, password, email):
        super().__init__(None, username, password, email)
        # Private attributes (-) as per diagram
        self.__officerID = f"OFF{Officer.off_counter:03d}"
        self.__email = email
        self.__name = username
        Officer.off_counter += 1

    # Method 1: generateCarbonEmissionReport()
    # Calculates sustainability impact based ONLY on delivered status.
    # Formula: CO2 (kg) = Distance (km) * 0.27
    def generateCarbonEmissionReport(self, all_deliveries):
        print("\n" + "="*50)
        print(f"{'CARBON EMISSION REPORT':^50}")
        print("="*50)
        
        total_co2 = 0
        delivered_count = 0

        # Iterating through all deliveries provided by the system
        for d_id, data in all_deliveries.items():
            # We only calculate for completed trips (either Delivered or Confirmed by VC)
            status = data.get('status')
            if status == "Delivered" or status == "Confirmed by VC":
                dist = data.get('distance', 0)
                # Applying the car emission formula from case study
                co2_val = dist * 0.27
                
                total_co2 += co2_val
                delivered_count += 1
                print(f"ID: {d_id:<10} | Distance: {dist:>4}km | CO2: {co2_val:.2f}kg")

        print("-" * 50)
        print(f"Total Successfully Delivered: {delivered_count}")
        print(f"Total Session Carbon Emission: {total_co2:.2f} kg CO2")
        print("="*50)

    # Method 2: viewPaymentReport()
    # Audits the payment report data from VC and verifies farmer payouts.
    def viewPaymentReport(self, vc_report_data):
        print("\n" + "="*45)
        print(f"{'OFFICER REPORT: FARMER PAYOUTS':^45}")
        print("="*45)
        
        if not vc_report_data:
            print("No financial records found for this period.")
            return

        total_payout = 0
        for entry in vc_report_data:
            print(f"Delivery {entry['id']}: Net Payout RM{entry['net']:.2f}")
            total_payout += entry['net']
            
        print("-" * 45)
        print(f"AUDIT TOTAL: RM{total_payout:.2f} verified.")
        print("="*45)

    # Method 3: viewOrderStatus()
    # Checks the global queue for orders not yet assigned by the VC.
    def viewOrderStatus(self, pending_list):
        print("\n--- [OFFICER] GLOBAL ORDER STATUS ---")
        if not pending_list:
            print("Current Status: All orders have been processed.")
        else:
            print(f"Warning: {len(pending_list)} orders are still awaiting VC assignment.")
            for order in pending_list:
                print(f" - {order['delivery_id']}: RM{order['price']} for {order['address']}")


# Class Officer Implemented by Muhammad Syafrul Hadzim Bin Mohamad Azlan (99983)