import tkinter as tk
import random
import heapq
import math

CELL_SIZE = 20
COLS = 30
ROWS = 20

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.walls = {"top": True, "right": True, "bottom": True, "left": True}
        self.visited = False

    def remove_wall(self, other, wall):
        self.walls[wall] = False
        opposite = {"top": "bottom", "right": "left", "bottom": "top", "left": "right"}
        other.walls[opposite[wall]] = False

class MazeGenerator:
    def __init__(self, cols, rows):
        self.cols = cols
        self.rows = rows
        self.grid = [[Cell(x, y) for y in range(rows)] for x in range(cols)]
        self.stack = []

    def index(self, x, y):
        if x < 0 or y < 0 or x >= self.cols or y >= self.rows:
            return None
        return self.grid[x][y]

    def get_neighbors(self, cell):
        neighbors = []
        directions = [("top", (0, -1)), ("right", (1, 0)), ("bottom", (0, 1)), ("left", (-1, 0))]
        for direction, (dx, dy) in directions:
            neighbor = self.index(cell.x + dx, cell.y + dy)
            if neighbor and not neighbor.visited:
                neighbors.append((direction, neighbor))
        return neighbors

    def generate_maze(self):
        current = self.grid[0][0]
        current.visited = True
        while True:
            neighbors = self.get_neighbors(current)
            if neighbors:
                direction, next_cell = random.choice(neighbors)
                next_cell.visited = True
                self.stack.append(current)
                current.remove_wall(next_cell, direction)
                current = next_cell
            elif self.stack:
                current = self.stack.pop()
            else:
                break

class MazeSolver:
    def __init__(self, grid):
        self.grid = grid
        self.cols = len(grid)
        self.rows = len(grid[0])

    def heuristic(self, cell, goal):
        return abs(cell.x - goal.x) + abs(cell.y - goal.y)

    def get_neighbors(self, cell):
        neighbors = []
        directions = {
            "top": (0, -1),
            "right": (1, 0),
            "bottom": (0, 1),
            "left": (-1, 0)
        }
        for direction, (dx, dy) in directions.items():
            if not cell.walls[direction]:
                neighbor = self.grid[cell.x + dx][cell.y + dy]
                neighbors.append(neighbor)
        return neighbors

    def solve(self, start, goal):
        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, goal)}

        while open_set:
            current = heapq.heappop(open_set)[1]
            if current == goal:
                return self.reconstruct_path(came_from, current)
            for neighbor in self.get_neighbors(current):
                tentative_g_score = g_score.get(current, float('inf')) + 1
                i
