# This is a deliberately poorly implemented main script for a Library Management System.
from check import Library

library_obj = Library()
def main_menu():
    print("\nLibrary Management System")
    print("1. Add Book")
    print("2. List Books")
    print("3. Add User")
    print("4. Checkout Book")
    print("5. Exit")
    choice = input("Enter choice: ")
    return choice

def main():
    while True:
        choice = main_menu()
        if choice == '1':
            title = input("Enter title: ")
            author = input("Enter author: ")
            isbn = input("Enter ISBN: ")
            library_obj.add_book(title, author, isbn)

        elif choice == '2':
            library_obj.list_books()
            
        elif choice == '3':
            name = input("Enter user name: ")
            user_id = input("Enter user ID: ")
            library_obj.add_user(user_id, name)

        elif choice == '4':
            user_id = input("Enter user ID: ")
            isbn = input("Enter ISBN of the book to checkout: ")
            library_obj.check_out_book(isbn, user_id)
            
        elif choice == '5':
            print("Exiting.")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
