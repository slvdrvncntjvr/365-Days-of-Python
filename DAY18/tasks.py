import os

def load_tasks():
    if not os.path.exists('data/tasks.txt'):
        return []
    
    with open('data/tasks.txt', 'r') as file:
        tasks = file.readlines()
    
    return [task.strip() for task in tasks]

def save_tasks(tasks):
    with open('data/tasks.txt', 'w') as file:
        for task in tasks:
            file.write(task + '\n')

def add_task(task):
    tasks = load_tasks()
    tasks.append(task)
    save_tasks(tasks)
    print("Task added.")

def view_tasks():
    tasks = load_tasks()
    if not tasks:
        print("No tasks found.")
        return
    print("\nYour Tasks:")
    for idx, task in enumerate(tasks, 1):
        print(f"{idx}. {task}")
