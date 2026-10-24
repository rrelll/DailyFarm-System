from user import User

class Driver(User):
    driver_counter = 1
    def __init__(self, username, password, email, contact=None):
        super().__init__(None, username, password, email)
        self._driverId = f"D{Driver.driver_counter:03d}"
        Driver.driver_counter += 1
        self.__contactNumber = contact

        self.availabilityStatus = "Available"
        self.assigned_deliveries = {}

    def get_contact(self):
        return self.__contactNumber

    def set_contact(self, contact):
        self.__contactNumber = contact

    def set_availability(self, available: bool):
        self.availabilityStatus = "Available" if available else "Unavailable"

    def update_delivery_status(self, delivery_id, status):
        if delivery_id in self.assigned_deliveries:
            self.assigned_deliveries[delivery_id] = status
            return True
        return False

    # Task 1: View Assigned Deliveries
    def viewAssignedDeliveries(self):
        print(f"\n--- Delivery List for {self._userId} ---")
        if not self.assigned_deliveries:
            print("No deliveries assigned at the moment.")
        for delivery_id, data in self.assigned_deliveries.items():
            # Handle both dict and string formats for backwards compatibility
            if isinstance(data, dict):
                status = data.get('status', 'Unknown')
            else:
                status = data
            print(f"Delivery ID: {delivery_id} | Status: [{status}]")

    # Task 2: Update Delivery Status
    def updateDeliveryStatus(self, delivery_id, new_status):
        if delivery_id in self.assigned_deliveries:
            # If it's a dict, update just the status field; otherwise replace
            if isinstance(self.assigned_deliveries[delivery_id], dict):
                self.assigned_deliveries[delivery_id]['status'] = new_status
            else:
                self.assigned_deliveries[delivery_id] = new_status
            print(f"Successfully updated {delivery_id} to: {new_status}")
        else:
            print(f"Error: Delivery ID {delivery_id} not found.")

    # Task 3: Update Availability 
    def updateAvailability(self, new_status):
        self.availabilityStatus = new_status
        print(f"Driver status is now set to: {self.availabilityStatus}")


# Class Driver Implemented by Theban A/L Vevindran (106554)
