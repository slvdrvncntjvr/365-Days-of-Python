class ExpenseTracker:
    def __init__(self):
        self.expenses = []

    def add_expense(self, description, amount, category):
        expense = {"description": description, "amount": amount, "category": category}
        self.expenses.append(expense)
        print(f"Expense added: {description} - ${amount} ({category})")

    def view_expenses(self):
        if not self.expenses:
            print("No expenses to show.")
            return
        print("\n--- Expenses ---")
        for i, expense in enumerate(self.expenses):
            print(f"{i}. {expense['description']} - ${expense['amount']} ({expense['category']})")

    def delete_expense(self, index):
        if 0 <= index < len(self.expenses):
            removed = self.expenses.pop(index)
            print(f"Removed expense: {removed['description']} - ${removed['amount']} ({removed['category']})")
        else:
            print("Invalid index. No expense deleted.")

    def total_expenses(self):
        return sum(expense["amount"] for expense in self.expenses)
