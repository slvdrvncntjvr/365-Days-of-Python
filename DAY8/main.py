from library import Library
from utils import get_valid_input

# Initialize the Library
library = Library()

def main():
    while True:
        print("\n--- Library Management System ---")
        print("1. Add a Book")
        print("2. View All Books")
        print("3. Borrow a Book")
        print("4. Return a Book")
        print("5. Exit")
        
        choice = get_valid_input("Choose an option (1-5): ", int, range(1, 6))
        
        if choice == 1:
            book_name = input("Enter the name of the book: ")
            author_name = input("Enter the author's name: ")
            library.add_book(book_name, author_name)
        elif choice == 2:
            library.view_books()
        elif choice == 3:
            book_name = input("Enter the name of the book to borrow: ")
            user_name = input("Enter your name: ")
            library.borrow_book(book_name, user_name)
        elif choice == 4:
            book_name = input("Enter the name of the book to return: ")
            user_name = input("Enter your name: ")
            library.return_book(book_name, user_name)
        elif choice == 5:
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()
