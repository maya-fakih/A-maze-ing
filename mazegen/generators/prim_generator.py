from typing import Any
from .maze_generator import MazeGenerator
import random


class PrimGenerator(MazeGenerator):
    """Prim's algorithm"""

    def __init__(self, settings_dict):
        super().__init__(settings_dict)

    def generate(self) -> Any:
        start = self.entry
        fringe = []

        for cell in self.logo_cells:
            x, y = cell
            self.path.append((cell, self.maze[x][y], False))
            self.visited.add(cell)

        self.initialize_maze()

        self.visited.add(start)

        for nx, ny, direction in self.get_neighbors(start):
            if (nx, ny) not in self.visited:
                fringe.append((nx, ny, direction, start))

        while fringe:
            idx = random.randint(0, len(fringe) - 1)
            nx, ny, direction, current = fringe.pop(idx)

            if (nx, ny) in self.visited:
                continue

            self.remove_wall(current, direction)
            self.visited.add((nx, ny))

            for nnx, nny, new_direction in self.get_neighbors((nx, ny)):
                if (nnx, nny) not in self.visited:
                    fringe.append((nnx, nny, new_direction, (nx, ny)))

        print("Maze generated using Prim's algorithm.")
        self.find_solution_path()

        if self.perfect is False:
            self.create_loops()
