import json

class Storage:
    def __init__(self, books_file='books.json', users_file='users.json'):
        """
        Initializes the Storage object with file paths for storing books and users data.

        Parameters:
        books_file (str): Path to the JSON file for storing books data.
        users_file (str): Path to the JSON file for storing users data.
        """
        self.books_file = books_file
        self.users_file = users_file

    def save_books(self, books):
        """
        Saves the list of books to a JSON file.

        Parameters:
        books (list): A list of Book objects to be saved.
        """
        try:
            with open(self.books_file, 'w') as f:
                json.dump([book.to_dict() for book in books], f, indent=4)
        except IOError as e:
            print(f"An error occurred while saving books: {e}")

    def load_books(self):
        """
        Loads the list of books from a JSON file.

        Returns:
        list: A list of Book objects.
        """
        try:
            from book import Book
            with open(self.books_file, 'r') as f:
                return [Book.from_dict(data) for data in json.load(f)]
        except FileNotFoundError:
            print(f"{self.books_file} not found. Returning an empty list.")
            return []
        except json.JSONDecodeError as e:
            print(f"An error occurred while loading books: {e}")
            return []

    def save_users(self, users):
        """
        Saves the list of users to a JSON file.

        Parameters:
        users (list): A list of User objects to be saved.
        """
        try:
            with open(self.users_file, 'w') as f:
                json.dump([user.to_dict() for user in users], f, indent=4)
        except IOError as e:
            print(f"An error occurred while saving users: {e}")

    def load_users(self):
        """
        Loads the list of users from a JSON file.

        Returns:
        list: A list of User objects.
        """
        try:
            from user import User
            with open(self.users_file, 'r') as f:
                return [User.from_dict(data) for data in json.load(f)]
        except FileNotFoundError:
            print(f"{self.users_file} not found. Returning an empty list.")
            return []
        except json.JSONDecodeError as e:
            print(f"An error occurred while loading users: {e}")
            return []
