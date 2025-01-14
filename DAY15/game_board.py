#when am i going to do this

import random

class GameBoard:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.food_position = None
    
    def place_food(self, snake_body):
        while True:
            y = random.randint(0, self.height - 1)
            x = random.randint(0, self.width - 1)
            if (y, x) not in snake_body:
                self.food_position = (y, x)
                break
