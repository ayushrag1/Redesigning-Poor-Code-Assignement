from storage import Storage
from logger import Logger

class User:
    def __init__(self, user_id, name, **kwargs):
        """
        Initializes a new User instance with required and optional attributes.

        Parameters:
        user_id (str): Unique identifier for the user.
        name (str): Name of the user.
        **kwargs: Additional attributes for the user (e.g., location, dob).
        """
        self.user_id = user_id
        self.name = name
        self.additional_attributes = kwargs  # Store any additional attributes

    def __str__(self):
        """
        Returns a string representation of the User instance.
        
        Returns:
        str: A string with the user's details.
        """
        details = f"User: {self.name} (ID: {self.user_id})"
        for key, value in self.additional_attributes.items():
            details += f", {key.capitalize()}: {value}"
        return details

    def to_dict(self):
        """
        Converts the User object to a dictionary for JSON serialization.

        Returns:
        dict: The dictionary representation of the User object.
        """
        data = {
            "user_id": self.user_id,
            "name": self.name
        }
        data.update(self.additional_attributes)
        return data

    @classmethod
    def from_dict(cls, data):
        """
        Creates a User object from a dictionary.

        Parameters:
        data (dict): The dictionary containing user data.

        Returns:
        User: A new User instance created from the dictionary data.
        """
        user_id = data.pop("user_id")
        name = data.pop("name")
        return cls(user_id, name, **data)


class ManageUsers:
    def __init__(self) -> None:
        """
        Initializes the ManageUsers instance, loading users from storage.
        """
        self.storage = Storage(users_file='users.json')
        self.users = self.storage.load_users()
        self.logger = Logger("users.log")

    def add_user(self, user_id, name, **kwargs):
        """
        Adds a new user to the system or updates an existing user.

        Parameters:
        user_id (str): Unique identifier for the user.
        name (str): Name of the user.
        **kwargs: Additional attributes for the user (e.g., location, dob).
        """
        try:
            if any(user.user_id == user_id for user in self.users):
                print(f"User with ID {user_id} already exists.")
                return
            
            new_user = User(user_id, name, **kwargs)
            self.users.append(new_user)
            self.storage.save_users(self.users)
            self.logger.log(f"Added user: {new_user}")
            print(f"User added: {new_user}")
        except Exception as e:
            print(f"An error occurred while adding a user: {e}")
            self.logger.log(f"Error while adding user: {e}")

    def list_users(self):
        """
        Lists all users currently in the system.
        """
        if not self.users:
            print("No users in the system.")
        else:
            for user in self.users:
                print(user)

    def search_users(self, keyword, parameter=""):
        """
        Searches for users by a specific parameter and keyword.

        Parameters:
        parameter (str): The attribute to search by (e.g., name, user_id).
        keyword (str): The keyword to search for in the specified attribute.
        """
        try:
            results = []
            if parameter == "name":
                results = [user for user in self.users if keyword.lower() in user.name.lower()]
            elif parameter == "user_id":
                results = [user for user in self.users if keyword == user.user_id]
            else:
                for user in self.users:
                    if parameter in user.additional_attributes and keyword.lower() in str(user.additional_attributes[parameter]).lower():
                        results.append(user)
                    elif keyword.lower() in user.name.lower() or keyword == user.user_id:
                        results.append(user)

            if results:
                for user in results:
                    print(user)
            else:
                print(f"No users found for {parameter}: {keyword}")
        except Exception as e:
            print(f"An error occurred during user search: {e}")
            self.logger.log(f"Error during user search: {e}")

    def update_user(self, user_id, **kwargs):
        """
        Updates a user's information based on the user ID.

        Parameters:
        user_id (str): The ID of the user to update.
        **kwargs: Attributes to update (e.g., name, location).
        """
        try:
            user = next((u for u in self.users if u.user_id == user_id), None)
            if user:
                if 'name' in kwargs:
                    user.name = kwargs['name']
                user.additional_attributes.update({k: v for k, v in kwargs.items() if k != 'name'})
                self.storage.save_users(self.users)
                self.logger.log(f"Updated user: {user}")
                print(f"User updated: {user}")
            else:
                print(f"User with ID {user_id} not found.")
        except Exception as e:
            print(f"An error occurred while updating the user: {e}")
            self.logger.log(f"Error while updating user: {e}")

    def delete_user(self, user_id):
        """
        Deletes a user from the system based on the user ID.

        Parameters:
        user_id (str): The ID of the user to delete.
        """
        try:
            user = next((u for u in self.users if u.user_id == user_id), None)
            if user:
                self.users.remove(user)
                self.storage.save_users(self.users)
                self.logger.log(f"Deleted user: {user}")
                print(f"User deleted: {user}")
            else:
                print(f"User with ID {user_id} not found.")
        except Exception as e:
            print(f"An error occurred while deleting the user: {e}")
            self.logger.log(f"Error while deleting user: {e}")
