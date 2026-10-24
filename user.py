# Superclass: User
class User:
    user_counter = 1
    def __init__(self, userId=None, username=None, password=None, email=None):
        if userId is None:
            userId = f"U{User.user_counter:03d}"
            User.user_counter += 1
        self._userId = userId         # Protected
        self.__username = username    # Private
        self.__password = password    # Private
        self.__email = email          # Private

# Method to Verify login credentials
    def login(self, username, password):
        return self.__username == username and self.__password == password

    def get_username(self):
        return self.__username

# Method to Display user dashboard
    def displayDashboard(self):
        print(f"Displaying dashboard for user ID {self._userId}")

# Class User Implemented by Darryl Anak Staban Lanjang (103794)