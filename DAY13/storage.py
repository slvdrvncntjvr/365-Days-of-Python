import json
import os

FOLDER_PATH = "Day13"
FILE_PATH = os.path.join(FOLDER_PATH, "tasks.json")

def ensure_folder_exists():
    if not os.path.exists(FOLDER_PATH):
        os.makedirs(FOLDER_PATH)

def load_tasks():
    ensure_folder_exists()
    if os.path.exists(FILE_PATH):
        try:
            with open(FILE_PATH, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            print("Error reading tasks file. Starting with an empty list.")
            return []
    return []

def save_tasks(tasks):
    ensure_folder_exists()
    with open(FILE_PATH, "w") as file:
        json.dump(tasks, file, indent=4)
