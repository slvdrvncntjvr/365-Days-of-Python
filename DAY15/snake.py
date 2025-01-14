# snake.py

class Snake:
    def __init__(self, initial_position, initial_length):
        self.body = [initial_position]  
        self.direction = (0, 1)       
        self.grow_next = 0             
    
    def move(self):
        head_y, head_x = self.body[0]
        dir_y, dir_x = self.direction
        new_head = (head_y + dir_y, head_x + dir_x)

        self.body.insert(0, new_head) 
        if self.grow_next > 0:
            self.grow_next -= 1        
        else:
            self.body.pop()           
    
    def grow(self): #reproduce
        self.grow_next += 1
    
    def set_direction(self, new_direction):
        dir_y, dir_x = new_direction
        if (dir_y, dir_x) == (-self.direction[0], -self.direction[1]):
            return 
        self.direction = new_direction

    def has_collision(self, board_width, board_height):
        head_y, head_x = self.body[0]
        if head_y < 0 or head_y >= board_height or head_x < 0 or head_x >= board_width:
            return True
        if (head_y, head_x) in self.body[1:]:
            return True
        return False
