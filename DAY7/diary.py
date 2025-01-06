import os
from cryptography.fernet import Fernet

FOLDER_PATH = os.path.join(os.path.dirname(__file__), "Diary Config")

if not os.path.exists(FOLDER_PATH):
    os.makedirs(FOLDER_PATH)

def generate_key():
    key_path = os.path.join(FOLDER_PATH, "secret.key")
    if not os.path.exists(key_path):
        key = Fernet.generate_key()
        with open(key_path, "wb") as key_file:
            key_file.write(key)

def load_key():
    key_path = os.path.join(FOLDER_PATH, "secret.key")
    with open(key_path, "rb") as key_file:
        return key_file.read()

def encrypt_message(message, key):
    fernet = Fernet(key)
    return fernet.encrypt(message.encode())

def decrypt_message(encrypted_message, key):
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_message).decode()

def save_entry(entry):
    key = load_key()
    encrypted_entry = encrypt_message(entry, key)
    diary_path = os.path.join(FOLDER_PATH, "diary.txt")
    with open(diary_path, "ab") as file:
        file.write(encrypted_entry + b"\n")

def view_entries():
    key = load_key()
    diary_path = os.path.join(FOLDER_PATH, "diary.txt")
    if not os.path.exists(diary_path):
        print("No entries found.")
        return

    with open(diary_path, "rb") as file:
        entries = file.readlines()
        for i, encrypted_entry in enumerate(entries, start=1):
            decrypted_entry = decrypt_message(encrypted_entry.strip(), key)
            print(f"Entry {i}: {decrypted_entry}")

def main():
    generate_key()

    while True:
        print("\n--- Encrypted Personal Diary ---")
        print("1. Add a new entry")
        print("2. View all entries")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            entry = input("Write your diary entry: ")
            save_entry(entry)
            print("Entry saved securely!")
        elif choice == "2":
            print("\nYour Diary Entries:")
            view_entries()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()