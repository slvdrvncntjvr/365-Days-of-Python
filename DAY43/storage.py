import json
import os

DAY_FOLDER = "DAY43"
DATA_FILE = os.path.join(DAY_FOLDER, "data.json")

def load_data():
    if not os.path.exists(DATA_FILE):
        data = {"tasks": [], "sessions": {}}
        save_data(data)
        return data
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)
