import time

def start_timer(activity):
    print(f"Starting timer for: {activity}")
    start_time = time.time()
    
    input("Press Enter to stop the timer...\n")
    
    end_time = time.time()
    duration = end_time - start_time
    log_time(activity, duration)

def log_time(activity, duration):
    with open('data/time_log.txt', 'a') as file:
        file.write(f"{activity}: {duration / 60:.2f} minutes\n")
    print(f"Time logged for {activity}: {duration / 60:.2f} minutes")

def view_time_log():
    if not os.path.exists('data/time_log.txt'):
        print("No time log found.")
        return
    
    with open('data/time_log.txt', 'r') as file:
        logs = file.readlines()
    
    if not logs:
        print("No time logs found.")
        return
    
    print("\nTime Log:")
    for log in logs:
        print(log.strip())
