class GameMap:
    def __init__(self):
        self.map = {
            (0, 0): {"name": "Village Square", "description": "A bustling village center."},
            (0, 1): {"name": "Blacksmith's Forge", "description": "Tools and weapons are scattered around."},
            (1, 0): {"name": "Dark Forest", "description": "Tall trees block the sunlight."},
            (1, 1): {"name": "Ancient Ruins", "description": "Mysterious glyphs glow faintly."},
            (2, 1): {"name": "Hidden Cave", "description": "The air is damp and cold."},
        }
        self.player_position = (0, 0)

    def move_player(self, direction):
        x, y = self.player_position
        if direction == "north":
            new_position = (x, y + 1)
        elif direction == "south":
            new_position = (x, y - 1)
        elif direction == "east":
            new_position = (x + 1, y)
        elif direction == "west":
            new_position = (x - 1, y)
        else:
            print("Invalid direction.")
            return False

        if new_position in self.map:
            self.player_position = new_position
            print(f"You moved to: {self.map[new_position]['name']}")
            return True
        print("You can't go that way.")
        return False

    def get_current_location(self):
        return self.map[self.player_position]["name"]

    def get_location_description(self):
        return self.map[self.player_position]["description"]
