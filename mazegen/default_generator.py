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


    def is_perfect(self, cell) -> bool:
        if self.perfect is True:
            return (cell in self.visited)
        #else:
        #    choice = random.randint(1, 4)
        #    if choice == 1:
        #        return (cell in self.solution)
        #    if choice == 2:
        #        return (cell in self.visited)
        #    if choice == 3 or choice == 5:
        #        return (False)
        #    if choice == 4:
        #        return (True)
        return (cell in self.solution)

    def generate(self) -> Any:
        start = self.entry
        fringe = []

        for cell in self.logo_cells:
            x, y = cell
            self.path.append((cell, self.maze[x][y], False))
            self.visited.add(cell)

        self.initialize_maze()

        self.visited.add(start)
        self.solution[start] = None
        
        for nx, ny, direction in self.get_neighbors(start):
            if (nx, ny) not in self.visited:
                fringe.append((nx, ny, direction, start))

        while fringe:
            idx = random.randint(0, len(fringe) - 1)
            nx, ny, direction, current = fringe.pop(idx)
            
            if self.is_perfect((nx, ny)):
                continue
            
            self.remove_wall(current, direction)
            self.visited.add((nx, ny))
            self.solution[(nx, ny)] = current
            
            for nnx, nny, new_direction in self.get_neighbors((nx, ny)):
                if (nnx, nny) not in self.visited:
                    fringe.append((nnx, nny, new_direction, (nx, ny)))

        if self.exit in self.solution:
            print("exit reached")
            solution_cells = set()
            current = self.exit
            while current is not None:
                solution_cells.add(current)
                current = self.solution[current]

            for cell in self.visited:
                x, y = cell
                if cell == start:
                    self.path.append((cell, self.maze[x][y], True))
                elif cell in solution_cells:
                    self.path.append((cell, self.maze[x][y], True))
                else:
                    self.path.append((cell, self.maze[x][y], False))
        else:
            for cell in self.visited:
                x, y = cell
                self.path.append((cell, self.maze[x][y], False))