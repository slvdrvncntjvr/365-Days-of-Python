from typing import List  # Import List for type annotations
import random

def get_user_input(prompt: str) -> str:
    return input(prompt).strip().lower()

def random_event_trigger(chance: float) -> bool:
    return random.random() < chance

def format_items_list(items: List[str]) -> str:
    return ', '.join(items) if items else 'nothing'