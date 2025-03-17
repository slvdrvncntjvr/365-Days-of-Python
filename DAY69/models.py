from typing import List, Dict, Optional

class Player:
    def __init__(self, name: str):
        self.name = name
        self.inventory: List[str] = []
        self.position: str = 'start'

    def move(self, new_position: str):
        self.position = new_position

    def add_item(self, item: str):
        self.inventory.append(item)

class Environment:
    def __init__(self):
        self.locations: Dict[str, Dict[str, str]] = {
            'start': {'description': 'You are in a dark forest. Paths lead north and east.', 'items': ['map']},
            'north': {'description': 'You find yourself at the edge of a serene lake.', 'items': []},
            'east': {'description': 'A rocky path leads to a mysterious cave.', 'items': ['torch']}
        }
        self.dynamic_events: Dict[str, str] = {
            'lake_monster': 'A monster emerges from the lake!',
            'cave_collapse': 'The cave entrance collapses behind you!'
        }

    def get_description(self, location: str) -> str:
        return self.locations.get(location, {}).get('description', 'Unknown location')

    def get_items(self, location: str) -> List[str]:
        return self.locations.get(location, {}).get('items', [])

    def trigger_event(self, event_key: str) -> Optional[str]:
        return self.dynamic_events.get(event_key)