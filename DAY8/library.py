class Library:
    def __init__(self):
        self.books = []  # List of books in the library

    def add_book(self, book_name, author_name):
        book = {"name": book_name, "author": author_name, "borrowed_by": None}
        self.books.append(book)
        print(f"Book '{book_name}' by {author_name} added to the library.")

    def view_books(self):
        if not self.books:
            print("No books available in the library.")
            return
        print("\n--- Available Books ---")
        for book in self.books:
            status = f"Borrowed by {book['borrowed_by']}" if book["borrowed_by"] else "Available"
            print(f"{book['name']} by {book['author']} - {status}")

    def borrow_book(self, book_name, user_name):
        for book in self.books:
            if book["name"].lower() == book_name.lower():
                if book["borrowed_by"]:
                    print(f"Sorry, the book '{book_name}' is already borrowed by {book['borrowed_by']}.")
                else:
                    book["borrowed_by"] = user_name
                    print(f"Book '{book_name}' borrowed successfully by {user_name}.")
                return
        print(f"Sorry, the book '{book_name}' is not available in the library.")

    def return_book(self, book_name, user_name):
        for book in self.books:
            if book["name"].lower() == book_name.lower() and book["borrowed_by"] == user_name:
                book["borrowed_by"] = None
                print(f"Book '{book_name}' returned successfully by {user_name}.")
                return
        print(f"Sorry, the book '{book_name}' was not borrowed by {user_name}.")

