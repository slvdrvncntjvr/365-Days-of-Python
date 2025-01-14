import curses
import time
from snake import Snake
from game_board import GameBoard
from score import Score
from constants import *

def main(stdscr):
    # Setup curses
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(COLOR_SNAKE, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(COLOR_FOOD, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(COLOR_BORDER, curses.COLOR_WHITE, curses.COLOR_BLACK)


    board = GameBoard(BOARD_WIDTH, BOARD_HEIGHT)
    snake = Snake(initial_position=(BOARD_HEIGHT // 2, BOARD_WIDTH // 2),
                  initial_length=INITIAL_SNAKE_LENGTH)
    score = Score()

    board.place_food(snake.body)

    key_map = {curses.KEY_UP: (-1, 0), curses.KEY_DOWN: (1, 0),
               curses.KEY_LEFT: (0, -1), curses.KEY_RIGHT: (0, 1)}
    last_key = curses.KEY_RIGHT
    speed = INITIAL_SPEED

    while True:
        stdscr.clear()
        
        for x in range(BOARD_WIDTH + 2):
            stdscr.addch(0, x, '#', curses.color_pair(COLOR_BORDER))
            stdscr.addch(BOARD_HEIGHT + 1, x, '#', curses.color_pair(COLOR_BORDER))
        for y in range(BOARD_HEIGHT + 2):
            stdscr.addch(y, 0, '#', curses.color_pair(COLOR_BORDER))
            stdscr.addch(y, BOARD_WIDTH + 1, '#', curses.color_pair(COLOR_BORDER))

      
        for y, x in snake.body:
            stdscr.addch(y + 1, x + 1, 'O', curses.color_pair(COLOR_SNAKE))
        
        
        food_y, food_x = board.food_position
        stdscr.addch(food_y + 1, food_x + 1, '*', curses.color_pair(COLOR_FOOD))

      
        stdscr.addstr(0, BOARD_WIDTH + 3, f"Score: {score.score}")
        stdscr.addstr(1, BOARD_WIDTH + 3, f"Level: {score.level}")

        stdscr.refresh()

       
        try:
            key = stdscr.getch()
            if key in key_map:
                snake.set_direction(key_map[key])
        except:
            pass

  
        snake.move()

        if snake.has_collision(BOARD_WIDTH, BOARD_HEIGHT):
            break

        
        if snake.body[0] == board.food_position:
            score.increase()
            snake.grow()
            board.place_food(snake.body)

       
        speed = INITIAL_SPEED / score.level
        time.sleep(speed)

if __name__ == "__main__":
    curses.wrapper(main)
