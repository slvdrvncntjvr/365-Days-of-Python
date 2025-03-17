from models import Player, Environment
from utils import get_user_input, random_event_trigger, format_items_list

def main():
    player_name = get_user_input("Enter your character's name: ")
    player = Player(name=player_name)
    env = Environment()

    print(f"Welcome, {player.name}, to the Adventure Game!")

    while True:
        location = player.position
        description = env.get_description(location)
        items = env.get_items(location)

        print(f"\nLocation: {location.capitalize()}")
        print(description)
        print(f"You see: {format_items_list(items)}")

        if items:
            take_item = get_user_input("Do you want to take the items? (yes/no): ")
            if take_item == 'yes':
                for item in items:
                    player.add_item(item)
                env.locations[location]['items'] = []

        move = get_user_input("Where do you want to go? (north/east/quit): ")
        if move in env.locations:
            player.move(move)
        elif move == 'quit':
            print("Thanks for playing!")
            break
        else:
            print("Invalid direction.")

        # Trigger random events
        if location == 'north' and random_event_trigger(0.3):
            event = env.trigger_event('lake_monster')
            print(event)
        elif location == 'east' and random_event_trigger(0.5):
            event = env.trigger_event('cave_collapse')
            print(event)

if __name__ == "__main__":
    main()