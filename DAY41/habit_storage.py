import json
from typing import List, Dict

def load_habits(filename: str) -> List[Dict]:
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_habits(filename: str, habits: List[Dict]) -> None:
    with open(filename, 'w') as file:
        json.dump(habits, file, indent=4)