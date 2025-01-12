from storage import load_tasks, save_tasks

def display_menu():
    print("\n=== To-Do List Manager ===")
    print("1. View all tasks")
    print("2. Add a task")
    print("3. Mark a task as complete")
    print("4. Delete a task")
    print("5. Exit")

def view_tasks(tasks):
    if not tasks:
        print("\nNo tasks found!")
    else:
        print("\nYour Tasks:")
        for idx, task in enumerate(tasks, start=1):
            status = "✓" if task['completed'] else "✗"
            print(f"{idx}. [{status}] {task['description']}")

def add_task(tasks):
    description = input("\nEnter the task description: ").strip()
    if description:
        tasks.append({"description": description, "completed": False})
        print(f"Task '{description}' added successfully!")
    else:
        print("Task description cannot be empty.")

def mark_task_complete(tasks):
    view_tasks(tasks)
    if tasks:
        try:
            task_num = int(input("\nEnter the task number to mark as complete: ")) - 1
            if 0 <= task_num < len(tasks):
                tasks[task_num]['completed'] = True
                print(f"Task '{tasks[task_num]['description']}' marked as complete!")
            else:
                print("Invalid task number.")
        except ValueError:
            print("Please enter a valid number.")

def delete_task(tasks):
    view_tasks(tasks)
    if tasks:
        try:
            task_num = int(input("\nEnter the task number to delete: ")) - 1
            if 0 <= task_num < len(tasks):
                deleted_task = tasks.pop(task_num)
                print(f"Task '{deleted_task['description']}' deleted successfully!")
            else:
                print("Invalid task number.")
        except ValueError:
            print("Please enter a valid number.")

def main():
    tasks = load_tasks()

    while True:
        display_menu()
        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            view_tasks(tasks)
        elif choice == "2":
            add_task(tasks)
        elif choice == "3":
            mark_task_complete(tasks)
        elif choice == "4":
            delete_task(tasks)
        elif choice == "5":
            save_tasks(tasks)
            print("Tasks saved. Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
