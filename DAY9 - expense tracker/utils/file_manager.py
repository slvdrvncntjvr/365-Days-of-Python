import json

def save_data(file_name, data):
    with open(file_name, "w") as file:
        json.dump(data, file, indent=4)
    print(f"Data saved to {file_name}.")

def load_data(file_name):
    try:
        with open(file_name, "r") as file:
            data = json.load(file)
        print(f"Data loaded from {file_name}.")
        return data
    except FileNotFoundError:
        print(f"{file_name} not found. Starting with an empty dataset.")
        return []
