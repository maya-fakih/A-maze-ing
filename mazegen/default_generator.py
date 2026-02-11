from typing import Any
from maze_generator import MazeGenerator
from collections import deque
import random


class BasicGenerator(MazeGenerator):
    """Prim's algorithm"""

    def __init__(self, settings_dict):
        super().__init__(settings_dict)

    def initialize_maze(self) -> None:
        for x in range(self.width):
            for y in range(self.height):
                if (x, y) not in self.logo_cells:
                    self.maze[x][y] = 15

    def generate(self) -> Any:
        reached_goal = False
        start = self.entry
        fringe = []

        for cell in self.logo_cells:
            x, y = cell
            self.path.append((cell, self.maze[x][y], False))

        self.initialize_maze()

        fringe.append(start)
        xi, yi = start
        self.path.append((start, self.maze[xi][yi], True))

        while fringe:
            if not reached_goal:
                current = fringe.pop()
            else:
                current = random.choice(fringe)
                fringe.remove(current)
            
            visited = [cell for cell, _, _ in self.path]
            
            possible_moves = []
            for nx, ny, direction in self.get_neighbors(current):
                if (self.has_wall(current, direction) and ((nx, ny) not in visited)):
                    possible_moves.append((nx, ny, direction))
                    fringe.append((nx, ny))
            
            if possible_moves:
                nx, ny, direction = random.choice(possible_moves)
                self.remove_wall(current, direction)
                
                is_solution = not reached_goal
                self.path.append(((nx, ny), self.maze[nx][ny], is_solution))
                
                fringe.append((nx, ny))
                
                if (nx, ny) == self.exit:
                    self.maze[nx][ny] = 0
                    reached_goal = True
            else:
                if not reached_goal:
                    for i in range(len(self.path)-1, -1, -1):
                        if self.path[i][0] == current and self.path[i][2] is True:
                            self.path[i] = (self.path[i][0], self.path[i][1], False)
                            break
