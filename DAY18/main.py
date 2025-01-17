import time
from tasks import add_task, view_tasks
from weather import fetch_weather
from time_tracker import start_timer, view_time_log

def main():
    print("Welcome to MyCLI Assistant!\n")
    while True:
        print("\nWhat would you like to do today?")
        print("1. Add a task")
        print("2. View tasks")
        print("3. Check weather")
        print("4. Start time tracker")
        print("5. View time log")
        print("6. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            task = input("Enter your task: ")
            add_task(task)
        elif choice == '2':
            view_tasks()
        elif choice == '3':
            city = input("Enter city for weather: ")
            fetch_weather(city)
        elif choice == '4':
            activity = input("Enter the activity you want to track: ")
            start_timer(activity)
        elif choice == '5':
            view_time_log()
        elif choice == '6':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
