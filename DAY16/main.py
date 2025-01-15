from player import Player
from map import GameMap
from game_logic import GameLogic

def main():
    print("Welcome to 'Mystery of the Forgotten Kingdom'!")
    print("Type 'help' anytime for commands.")
    
    player = Player("Adventurer")
    game_map = GameMap()
    logic = GameLogic(player, game_map)

    while player.is_alive():
        print(f"\n[Location: {game_map.get_current_location()}]")
        print(f"Health: {player.health} | Inventory: {', '.join(player.inventory) if player.inventory else 'Empty'}")
        command = input("> ").strip().lower()
        
        if command == "quit":
            print("Thanks for playing. Farewell.")
            break
        elif command == "help":
            print("Commands: move <direction>, look, inventory, use <item>, talk, solve, attack, quit")
        else:
            logic.process_command(command)

if __name__ == "__main__":
    main()
