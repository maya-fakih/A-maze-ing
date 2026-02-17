from typing import Any
from .maze_generator import MazeGenerator
import random


class DFSGenerator(MazeGenerator):
    """Depth First algorithm"""

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
        self.solution[start] = None

        possible = []
        for nx, ny, direction in self.get_neighbors(start):
            if (nx, ny) not in self.visited:
                possible.append((nx, ny, direction, start))
        random.shuffle(possible)
        fringe.extend(possible)

        while fringe:
            nx, ny, direction, current = fringe.pop()

            if (nx, ny) in self.visited:
                continue

            self.remove_wall(current, direction)
            self.visited.add((nx, ny))
            self.solution[(nx, ny)] = current

            neighbors = self.get_neighbors((nx, ny))
            random.shuffle(neighbors)

            for nnx, nny, new_direction in neighbors:
                possible_moves = []
                if (nnx, nny) not in self.visited:
                    possible_moves.append((nnx, nny, new_direction, (nx, ny)))

                random.shuffle(possible_moves)
                for move in possible_moves:
                    fringe.append(move)

        self.find_solution_path()

        if self.perfect is False:
            self.create_loops()
