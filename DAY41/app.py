from habit_storage import load_habits, save_habits
from habit_tracker import add_habit, remove_habit, log_progress, view_habits

def main():
    filename = 'habits.json'
    habits = load_habits(filename)

    while True:
        print("\nHabit Tracker")
        print("1. Add Habit")
        print("2. Remove Habit")
        print("3. Log Progress")
        print("4. View Habits")
        print("5. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            name = input("Enter habit name: ")
            add_habit(habits, name)
        elif choice == '2':
            name = input("Enter habit name to remove: ")
            remove_habit(habits, name)
        elif choice == '3':
            name = input("Enter habit name: ")
            date = input("Enter date of progress (YYYY-MM-DD): ")
            log_progress(habits, name, date)
        elif choice == '4':
            view_habits(habits)
        elif choice == '5':
            save_habits(filename, habits)
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()