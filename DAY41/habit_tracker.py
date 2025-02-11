from typing import List, Dict

def add_habit(habits: List[Dict], name: str) -> None:
    habit = {'name': name, 'progress': []}
    habits.append(habit)

def remove_habit(habits: List[Dict], name: str) -> None:
    habits[:] = [habit for habit in habits if habit['name'] != name]

def log_progress(habits: List[Dict], name: str, date: str) -> None:
    for habit in habits:
        if habit['name'] == name:
            habit['progress'].append(date)

def view_habits(habits: List[Dict]) -> None:
    for habit in habits:
        print(f"Habit: {habit['name']}, Progress: {habit['progress']}")