import os
import json
import base64
from datetime import datetime
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

ENTRIES_FILE = "journal_entries.json"
SECRET_CONSTANT = "my_super_secret_constant"

def derive_key(lock_date: str, salt: bytes) -> bytes:
    password = (lock_date + SECRET_CONSTANT).encode()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    return key

def encrypt_entry(text: str, lock_date: str) -> dict:
    salt = os.urandom(16)
    key = derive_key(lock_date, salt)
    cipher = Fernet(key)
    ciphertext = cipher.encrypt(text.encode()).decode()
    return {
        "lock_date": lock_date,
        "salt": base64.b64encode(salt).decode(),
        "ciphertext": ciphertext
    }

def decrypt_entry(entry: dict) -> str:
    lock_date = entry["lock_date"]
    if datetime.now() < datetime.fromisoformat(lock_date):
        return "Locked until " + lock_date
    salt = base64.b64decode(entry["salt"].encode())
    key = derive_key(lock_date, salt)
    cipher = Fernet(key)
    try:
        plaintext = cipher.decrypt(entry["ciphertext"].encode()).decode()
        return plaintext
    except Exception:
        return "Decryption failed."

def load_entries() -> list:
    if not os.path.exists(ENTRIES_FILE):
        return []
    with open(ENTRIES_FILE, "r") as f:
        return json.load(f)

def save_entries(entries: list):
    with open(ENTRIES_FILE, "w") as f:
        json.dump(entries, f, indent=4)

def add_entry(text: str, lock_date: str):
    entry = encrypt_entry(text, lock_date)
    entries = load_entries()
    entries.append(entry)
    save_entries(entries)

def list_entries() -> list:
    return load_entries()
