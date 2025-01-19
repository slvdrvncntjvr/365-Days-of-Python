import datetime
import json
import os
from recipe_suggestions import suggest_recipes

# Define the DAY20 folder
DAY_FOLDER = "DAY20"
FOOD_FILE = os.path.join(DAY_FOLDER, "food_inventory.json")

# Load inventory from the food_inventory.json file
def load_inventory():
    try:
        with open(FOOD_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Save updated inventory to food_inventory.json
def save_inventory(inventory):
    with open(FOOD_FILE, "w") as file:
        json.dump(inventory, file, indent=4)

# Add a new food item to the inventory
def add_food_item(inventory):
    item_name = input("Enter the name of the food item: ").strip()
    expiry_date_str = input("Enter expiry date (YYYY-MM-DD): ").strip()
    
    try:
        expiry_date = datetime.datetime.strptime(expiry_date_str, "%Y-%m-%d").date()
        inventory[item_name] = {"expiry_date": expiry_date_str, "status": "Fresh"}
        save_inventory(inventory)
        print(f"{item_name} added successfully!")
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")

# Check items that are nearing expiry
def check_expiring_items(inventory):
    today = datetime.date.today()
    expiring_items = []
    for item, details in inventory.items():
        expiry_date = datetime.datetime.strptime(details["expiry_date"], "%Y-%m-%d").date()
        days_left = (expiry_date - today).days
        if days_left <= 3 and details["status"] == "Fresh":
            expiring_items.append((item, days_left))
    
    if expiring_items:
        print("\nItems nearing expiry:")
        for item, days_left in expiring_items:
            print(f"  - {item}: {days_left} day(s) left")
    else:
        print("\nNo items nearing expiry.")

# Remove expired items from the inventory
def remove_expired_items(inventory):
    today = datetime.date.today()
    expired_items = [item for item, details in inventory.items() if datetime.datetime.strptime(details["expiry_date"], "%Y-%m-%d").date() < today]
    
    for item in expired_items:
        inventory[item]["status"] = "Expired"
    save_inventory(inventory)
    
    if expired_items:
        print("\nExpired items:")
        for item in expired_items:
            print(f"  - {item}")
    else:
        print("\nNo expired items.")

# Suggest recipes based on items nearing expiry
def suggest_recipes_for_expiring(inventory):
    today = datetime.date.today()
    expiring_items = [item for item, details in inventory.items() if (datetime.datetime.strptime(details["expiry_date"], "%Y-%m-%d").date() - today).days <= 3 and details["status"] == "Fresh"]
    
    if expiring_items:
        print("\nRecipes you can try with expiring items:")
        for recipe in suggest_recipes(expiring_items):
            print(f"  - {recipe['title']} ({recipe['image']})")
    else:
        print("\nNo expiring items for recipe suggestions.")

# Main logic
def main():
    inventory = load_inventory()
    
    while True:
        print("\nSmart Fridge Tracker Menu:")
        print("1. Add a food item")
        print("2. View expiring items")
        print("3. Remove expired items")
        print("4. Get recipe suggestions")
        print("5. Exit")
        
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            add_food_item(inventory)
        elif choice == "2":
            check_expiring_items(inventory)
        elif choice == "3":
            remove_expired_items(inventory)
        elif choice == "4":
            suggest_recipes_for_expiring(inventory)
        elif choice == "5":
            print("Exiting Smart Fridge Tracker. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
