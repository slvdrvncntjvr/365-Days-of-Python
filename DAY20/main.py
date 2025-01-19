import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import PhotoImage
import datetime
import json
import os
from recipe_suggestions import suggest_recipes

DAY_FOLDER = "DAY20"
FOOD_FILE = os.path.join(DAY_FOLDER, "food_inventory.json")

def load_inventory():
    try:
        with open(FOOD_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_inventory(inventory):
    with open(FOOD_FILE, "w") as file:
        json.dump(inventory, file, indent=4)

def add_food_item():
    def save_item():
        item_name = name_entry.get().strip()
        expiry_date_str = date_entry.get().strip()
        if not item_name or not expiry_date_str:
            messagebox.showerror("Error", "Both fields are required!")
            return

        try:
            expiry_date = datetime.datetime.strptime(expiry_date_str, "%Y-%m-%d").date()
            inventory[item_name] = {"expiry_date": expiry_date_str, "status": "Fresh"}
            save_inventory(inventory)
            messagebox.showinfo("Success", f"{item_name} added successfully!")
            add_window.destroy()
            refresh_inventory()
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD.")

    add_window = tk.Toplevel(root)
    add_window.title("Add Food Item")

    tk.Label(add_window, text="Food Item Name:").grid(row=0, column=0, padx=10, pady=10)
    name_entry = tk.Entry(add_window)
    name_entry.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(add_window, text="Expiry Date (YYYY-MM-DD):").grid(row=1, column=0, padx=10, pady=10)
    date_entry = tk.Entry(add_window)
    date_entry.grid(row=1, column=1, padx=10, pady=10)

    tk.Button(add_window, text="Add", command=save_item).grid(row=2, column=0, columnspan=2, pady=10)

def refresh_inventory():
    for item in tree.get_children():
        tree.delete(item)

    today = datetime.date.today()
    for item, details in inventory.items():
        expiry_date = datetime.datetime.strptime(details["expiry_date"], "%Y-%m-%d").date()
        days_left = (expiry_date - today).days
        status = details["status"]

        if days_left < 0:
            status = "Expired"
            inventory[item]["status"] = "Expired"
        elif days_left <= 3 and status == "Fresh":
            status = "Nearing Expiry"

        tree.insert("", "end", values=(item, details["expiry_date"], status))


def suggest_recipes_gui():
    today = datetime.date.today()
    expiring_items = [item for item, details in inventory.items() if (datetime.datetime.strptime(details["expiry_date"], "%Y-%m-%d").date() - today).days <= 3 and details["status"] == "Fresh"]

    if not expiring_items:
        messagebox.showinfo("No Suggestions", "No expiring items for recipe suggestions.")
        return

    recipes = suggest_recipes(expiring_items)

    recipe_window = tk.Toplevel(root)
    recipe_window.title("Recipe Suggestions")

    for recipe in recipes:
        frame = ttk.Frame(recipe_window)
        frame.pack(fill="x", padx=10, pady=5)

        img_label = tk.Label(frame, text=recipe["title"])
        img_label.pack(side="left")

        title_label = tk.Label(frame, text=recipe["title"], font=("Arial", 14))
        title_label.pack(side="left", padx=10)

root = tk.Tk()
root.title("Smart Fridge Tracker")

inventory = load_inventory()

columns = ("Item", "Expiry Date", "Status")
tree = ttk.Treeview(root, columns=columns, show="headings")
tree.heading("Item", text="Item")
tree.heading("Expiry Date", text="Expiry Date")
tree.heading("Status", text="Status")
tree.pack(fill="both", expand=True, padx=10, pady=10)

refresh_inventory()

btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Add Food Item", command=add_food_item).pack(side="left", padx=5)
tk.Button(btn_frame, text="Suggest Recipes", command=suggest_recipes_gui).pack(side="left", padx=5)

root.mainloop()
