from expense_tracker import ExpenseTracker
from utils.file_manager import save_data, load_data

expense_tracker = ExpenseTracker()
expense_tracker.expenses = load_data("expenses.json")

def main():
    while True:
        print("\n--- Expense Tracker ---")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. Delete Expense")
        print("4. Total Expense")
        print("5. Save and Exit")

        choice = input("Choose an option (1-5): ")

        if choice == "1":
            description = input("Enter expense description: ")
            amount = float(input("Enter expense amount: "))
            category = input("Enter expense category: ")
            expense_tracker.add_expense(description, amount, category)
        elif choice == "2":
            expense_tracker.view_expenses()
        elif choice == "3":
            index = int(input("Enter the index of the expense to delete: "))
            expense_tracker.delete_expense(index)
        elif choice == "4":
            print(f"Total Expense: {expense_tracker.total_expenses()}")
        elif choice == "5":
            save_data("expenses.json", expense_tracker.expenses)
            print("Data saved. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
