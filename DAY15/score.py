

class Score:
    def __init__(self):
        self.score = 0
        self.level = 1
    
    def increase(self):
        self.score += 10
        if self.score % 50 == 0:  # Every 50 points, level up
            self.level += 1
