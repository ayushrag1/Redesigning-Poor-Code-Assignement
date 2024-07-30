from book import ManageBooks
from user import ManageUsers
from logger import Logger

class Library(ManageUsers, ManageBooks):
    def __init__(self) -> None:
        # Initialize parent classes to load users and books
        ManageUsers.__init__(self)
        ManageBooks.__init__(self)
        self.logger = Logger("library.log")  # Logger for library-specific actions

    def search_books(self, keyword, parameter=""):
        """
        Search for books by a specific parameter (title, author, isbn) and keyword.

        Parameters:
        parameter (str): The attribute to search by (title, author, isbn, or any additional attribute).
        keyword (str): The keyword to search for in the specified attribute.
        """
        try:
            results = []
            if parameter in ["title", "author", "isbn"]:
                results = [book for book in self.books if keyword.lower() in getattr(book, parameter).lower()]
            else:
                # Search across all attributes including additional ones
                for book in self.books:
                    if (keyword.lower() in book.title.lower() or 
                        keyword.lower() in book.author.lower() or 
                        keyword.lower() in book.isbn.lower() or 
                        any(keyword.lower() in str(value).lower() for value in book.additional_attributes.values())):
                        results.append(book)

            if results:
                for book in results:
                    print(book)
            else:
                print(f"No books found for keyword: {keyword}")
        except Exception as e:
            print(f"An error occurred during book search: {e}")
            self.logger.log(f"Error during book search: {e}")

    def check_out_book(self, isbn, user_id):
        """
        Check out a book for a user by decreasing the available count of the book.

        Parameters:
        isbn (str): The ISBN of the book to be checked out.
        user_id (str): The ID of the user checking out the book.
        """
        try:
            book = next((b for b in self.books if b.isbn == isbn), None)
            user = next((u for u in self.users if u.user_id == user_id), None)
            
            if not book:
                print("Invalid book ISBN.")
                return
            if not user:
                print("Invalid user ID.")
                return

            if book.count > 0:
                book.count -= 1
                book.available = book.count > 0
                self.storage.save_books(self.books)
                self.logger.log(f"Book checked out: {book} by User: {user}")
                print(f"Book checked out: {book}")
            else:
                print(f"Book '{book.title}' is not available.")
        except Exception as e:
            print(f"An error occurred during book checkout: {e}")
            self.logger.log(f"Error during book checkout: {e}")

    def check_in_book(self, isbn):
        """
        Check in a book by increasing the available count of the book.

        Parameters:
        isbn (str): The ISBN of the book to be checked in.
        """
        try:
            book = next((b for b in self.books if b.isbn == isbn), None)
            if not book:
                print("Invalid book ISBN.")
                return

            book.count += 1
            book.available = True
            self.storage.save_books(self.books)
            self.logger.log(f"Book checked in: {book}")
            print(f"Book checked in: {book}")
        except Exception as e:
            print(f"An error occurred during book check-in: {e}")
            self.logger.log(f"Error during book check-in: {e}")
