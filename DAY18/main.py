from weather import get_weather

def display_dashboard():
    """
    Display the task dashboard for the user to interact with.
    """
    print("What would you like to do today?")
    print("1. Add a task")
    print("2. View tasks")
    print("3. Check weather")
    print("4. Start time tracker")
    print("5. View time log")
    print("6. Exit")

def main():
    """
    Main function to run the task manager and weather dashboard.
    """
    API_KEY = "f6554695744a0d1ad14435b91d143fd8"  
    
    while True:
        display_dashboard()
        choice = input("Enter your choice: ")

        if choice == "3":
            city = input("Enter city for weather: ")
            weather_data = get_weather(city, API_KEY)
            
            if weather_data:
                temperature, description = weather_data
                print(f"Weather in {city}: {temperature}°C, {description}")
            else:
                print("Failed to retrieve weather data.")
        
        elif choice == "6":
            print("Exiting the program.")
            break
        else:
            print("Option not implemented yet.")

if __name__ == "__main__":
    main()
