import sys
from datetime import datetime
from journal import add_entry, list_entries, decrypt_entry

def print_menu():
    print("\n=== Time Lock Journal ===")
    print("1. Add new journal entry")
    print("2. List all journal entries")
    print("3. View a specific entry")
    print("4. Exit")

def add_new_entry():
    text = input("Enter your journal entry:\n")
    lock_date = input("Enter unlock date (YYYY-MM-DD HH:MM:SS) or (YYYY-MM-DD):\n").strip()
    try:
        # Validate lock_date format
        datetime.fromisoformat(lock_date)
    except ValueError:
        print("Invalid date format.")
        return
    add_entry(text, lock_date)
    print("Entry added and encrypted.")

def list_all_entries():
    entries = list_entries()
    if not entries:
        print("No entries found.")
        return
    for idx, entry in enumerate(entries, 1):
        print(f"{idx}. Locked until: {entry['lock_date']}")

def view_entry():
    entries = list_entries()
    if not entries:
        print("No entries available.")
        return
    try:
        index = int(input("Enter entry number to view: ")) - 1
        if index < 0 or index >= len(entries):
            print("Invalid entry number.")
            return
        entry = entries[index]
        print("\n--- Journal Entry ---")
        print("Unlock Date:", entry["lock_date"])
        content = decrypt_entry(entry)
        print("Content:", content)
    except Exception as e:
        print("Error:", e)

def main():
    while True:
        print_menu()
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            add_new_entry()
        elif choice == "2":
            list_all_entries()
        elif choice == "3":
            view_entry()
        elif choice == "4":
            print("Exiting...")
            sys.exit(0)
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
