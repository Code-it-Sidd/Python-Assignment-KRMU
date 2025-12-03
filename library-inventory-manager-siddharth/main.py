import logging
from pathlib import Path

from inventory import LibraryInventory
from book import Book


def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
        handlers=[
            logging.FileHandler("library.log", encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )


def get_non_empty_input(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Input cannot be empty. Please try again.")


def add_book_cli(inventory: LibraryInventory) -> None:
    title = get_non_empty_input("Enter title: ")
    author = get_non_empty_input("Enter author: ")
    isbn = get_non_empty_input("Enter ISBN: ")
    book = Book(title=title, author=author, isbn=isbn)
    inventory.add_book(book)
    print("Book added successfully.")


def issue_book_cli(inventory: LibraryInventory) -> None:
    isbn = get_non_empty_input("Enter ISBN to issue: ")
    book = inventory.search_by_isbn(isbn)
    if not book:
        print("Book not found.")
        return
    if book.issue():
        inventory.save_to_file()
        logging.info("Book issued: %s", book)
        print("Book issued.")
    else:
        print("Book is already issued.")


def return_book_cli(inventory: LibraryInventory) -> None:
    isbn = get_non_empty_input("Enter ISBN to return: ")
    book = inventory.search_by_isbn(isbn)
    if not book:
        print("Book not found.")
        return
    if book.return_book():
        inventory.save_to_file()
        logging.info("Book returned: %s", book)
        print("Book returned.")
    else:
        print("Book was not issued.")


def search_cli(inventory: LibraryInventory) -> None:
    print("1. Search by Title")
    print("2. Search by ISBN")
    choice = input("Enter choice: ").strip()
    if choice == "1":
        title = get_non_empty_input("Enter title keyword: ")
        results = inventory.search_by_title(title)
        if not results:
            print("No books found.")
        else:
            for b in results:
                print(b)
    elif choice == "2":
        isbn = get_non_empty_input("Enter ISBN: ")
        book = inventory.search_by_isbn(isbn)
        if not book:
            print("Book not found.")
        else:
            print(book)
    else:
        print("Invalid choice.")


def view_all_cli(inventory: LibraryInventory) -> None:
    books = inventory.display_all()
    if not books:
        print("No books in inventory.")
    else:
        for b in books:
            print(b)


def main() -> None:
    configure_logging()
    storage_path = Path("data") / "books.json"

    try:
        inventory = LibraryInventory(storage_path)
    except Exception as exc:
        logging.error("Failed to initialize inventory: %s", exc)
        print("Critical error initializing inventory.")
        return

    while True:
        print("\n=== Library Menu ===")
        print("1. Add Book")
        print("2. Issue Book")
        print("3. Return Book")
        print("4. View All Books")
        print("5. Search")
        print("6. Exit")

        try:
            choice = input("Enter your choice (1-6): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting...")
            break

        try:
            if choice == "1":
                add_book_cli(inventory)
            elif choice == "2":
                issue_book_cli(inventory)
            elif choice == "3":
                return_book_cli(inventory)
            elif choice == "4":
                view_all_cli(inventory)
            elif choice == "5":
                search_cli(inventory)
            elif choice == "6":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 6.")
        except Exception as exc:
            logging.error("Unexpected error in menu loop: %s", exc)
        finally:
            # Could add periodic autosave or cleanup here
            pass


if __name__ == "__main__":
    main()
