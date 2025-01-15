from items import ITEMS
from random import randint

class GameLogic:
    def __init__(self, player, game_map):
        self.player = player
        self.game_map = game_map
        self.events_triggered = set()
        self.enemies = {"Dark Forest": {"health": 30, "damage": 5}}

    def process_command(self, command):
        if command.startswith("move "):
            direction = command.split(" ")[1]
            if self.game_map.move_player(direction):
                self.check_event()
        elif command == "look":
            print(self.game_map.get_location_description())
        elif command == "inventory":
            self.player.show_inventory()
        elif command.startswith("use "):
            item = command.split(" ", 1)[1]
            if self.player.use_item(item):
                print(f"You used the {item}.")
            else:
                print(f"You don't have {item}.")
        elif command == "talk":
            self.talk_to_npc()
        elif command == "solve":
            self.solve_puzzle()
        elif command == "attack":
            self.attack_enemy()
        else:
            print("Invalid command.")

    def check_event(self):
        location = self.game_map.get_current_location()
        if location == "Blacksmith's Forge" and "sword" not in self.events_triggered:
            print("You found a sword on the anvil!")
            self.player.add_item("sword")
            self.events_triggered.add("sword")
        elif location == "Dark Forest" and location not in self.events_triggered:
            print("An enemy emerges from the shadows!")
            self.events_triggered.add(location)

    def talk_to_npc(self):
        location = self.game_map.get_current_location()
        if location == "Village Square":
            print("Villager: Beware of the forest. Many have gone and never returned.")
        else:
            print("There's no one to talk to here.")

    def solve_puzzle(self):
        location = self.game_map.get_current_location()
        if location == "Ancient Ruins":
            print("A puzzle blocks your path. Solve it: What is 5 + 7?")
            answer = input("Answer: ")
            if answer == "12":
                print("The path opens!")
            else:
                print("The glyphs glow red. Try again later.")
        else:
            print("There's no puzzle here.")

    def attack_enemy(self):
        location = self.game_map.get_current_location()
        if location in self.enemies:
            enemy = self.enemies[location]
            damage = self.player.attack()
            enemy["health"] -= damage
            print(f"You hit the enemy for {damage} damage!")
            if enemy["health"] <= 0:
                print("You defeated the enemy!")
                del self.enemies[location]
            else:
                self.player.take_damage(enemy["damage"])
        else:
            print("There's nothing to attack here.")
