class Player:
    def __init__(self, name):
        self.name = name
        self.health = 100
        self.inventory = []
        self.damage = 10

    def add_item(self, item):
        self.inventory.append(item)
        print(f"Picked up: {item}")

    def use_item(self, item):
        if item in self.inventory:
            self.inventory.remove(item)
            return True
        return False

    def take_damage(self, amount):
        self.health -= amount
        print(f"You took {amount} damage!")
        if self.health <= 0:
            print("You have died.")
            return False
        return True

    def attack(self):
        return self.damage

    def is_alive(self):
        return self.health > 0

    def show_inventory(self):
        if self.inventory:
            print("Inventory:")
            for item in self.inventory:
                print(f"- {item}")
        else:
            print("Inventory is empty.")
