from storage import Storage
from logger import Logger

class Book:
    def __init__(self, title, author, isbn, count=1, available=True, **kwargs):
        """
        Initializes a new Book instance.

        Parameters:
        title (str): The title of the book.
        author (str): The author of the book.
        isbn (str): The ISBN of the book.
        count (int): The number of copies available. Defaults to 1.
        available (bool): Availability status of the book. Defaults to True.
        **kwargs: Additional attributes for the book (e.g., genre, year).
        """
        self.title = title
        self.author = author
        self.isbn = isbn
        self.count = count
        self.available = available
        self.additional_attributes = kwargs  # Store any additional attributes

    def __str__(self):
        details = f"{self.title} by {self.author} (ISBN: {self.isbn}, Count: {self.count}) - {'Available' if self.available else 'Checked out'}"
        for key, value in self.additional_attributes.items():
            details += f", {key.capitalize()}: {value}"
        return details

    def to_dict(self):
        """
        Converts the Book object to a dictionary for JSON serialization.

        Returns:
        dict: The dictionary representation of the Book object.
        """
        data = {
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "count": self.count,
            "available": self.available
        }
        data.update(self.additional_attributes)
        return data

    @classmethod
    def from_dict(cls, data):
        """
        Creates a Book object from a dictionary.

        Parameters:
        data (dict): The dictionary containing book data.

        Returns:
        Book: A new Book instance created from the dictionary data.
        """
        isbn = data.pop("isbn")
        title = data.pop("title")
        author = data.pop("author")
        count = data.pop("count", 1)
        available = data.pop("available", True)
        return cls(title, author, isbn, count, available, **data)


class ManageBooks:
    def __init__(self) -> None:
        """
        Initializes the ManageBooks instance, loading books from storage.
        """
        self.storage = Storage()
        self.books = self.storage.load_books()
        self.logger = Logger("books.log")

    def add_book(self, title, author, isbn, **kwargs):
        """
        Adds a new book to the library or increments the count if the book already exists.

        Parameters:
        title (str): The title of the book.
        author (str): The author of the book.
        isbn (str): The ISBN of the book.
        **kwargs: Additional attributes for the book (e.g., genre, year).
        """
        try:
            existing_book = next((book for book in self.books if book.isbn == isbn), None)
            if existing_book:
                existing_book.count += 1
                print(f"Book with ISBN {isbn} already exists. Incremented count to {existing_book.count}.")
            else:
                new_book = Book(title, author, isbn, **kwargs)
                self.books.append(new_book)
                print(f"Book added: {new_book}")

            self.storage.save_books(self.books)
            self.logger.log(f"Added/Updated book: {existing_book if existing_book else new_book}")
        except Exception as e:
            print(f"An error occurred while adding a book: {e}")
            self.logger.log(f"Error while adding/updating book: {e}")

    def list_books(self):
        """
        Lists all books currently in the library.
        """
        if not self.books:
            print("No books in the library.")
        else:
            for book in self.books:
                print(book)

    def update_book(self, isbn, new_title=None, new_author=None, new_count=None, **kwargs):
        """
        Updates a book's information based on the ISBN.

        Parameters:
        isbn (str): The ISBN of the book to update.
        new_title (str, optional): The new title of the book.
        new_author (str, optional): The new author of the book.
        new_count (int, optional): The new count of the book.
        **kwargs: Additional attributes to update for the book.
        """
        try:
            book = next((b for b in self.books if b.isbn == isbn), None)
            if book:
                if new_title:
                    book.title = new_title
                if new_author:
                    book.author = new_author
                if new_count is not None:
                    book.count = new_count
                book.additional_attributes.update(kwargs)
                self.storage.save_books(self.books)
                self.logger.log(f"Updated book: {book}")
                print(f"Book updated: {book}")
            else:
                print(f"Book with ISBN {isbn} not found.")
        except Exception as e:
            print(f"An error occurred while updating the book: {e}")
            self.logger.log(f"Error while updating book: {e}")
