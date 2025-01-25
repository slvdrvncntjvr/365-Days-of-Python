import csv
import datetime
import os

DAY_FOLDER = "DAY23"
FOOD_FILE = os.path.join(DAY_FOLDER, "mood_data.csv")

def display_menu():
    print("\nMood Tracker")
    print("1. Log Mood")
    print("2. Exit")

def log_mood():
    mood = input("How are you feeling today? (e.g., Happy, Sad, Anxious): ")
    notes = input("Any additional notes? ")
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    
    with open(FOOD_FILE, "a", newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date, mood, notes])
    print("Mood logged!")

def main():
    while True:
        display_menu()
        choice = input("Choose an option: ")
        if choice == '1':
            log_mood()
        elif choice == '2':
            print("Exiting the Mood Tracker. Take care!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()