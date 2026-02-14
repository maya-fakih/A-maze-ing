from typing import Any
from .maze_generator import MazeGenerator
import random


class HuntKillGenerator(MazeGenerator):
    """Hunt and Kill algorithm"""

    def __init__(self, settings_dict):
        super().__init__(settings_dict)

    def initialize_maze(self) -> None:
        for x in range(self.width):
            for y in range(self.height):
                if (x, y) not in self.logo_cells:
                    self.maze[x][y] = 15

    def hunt(self, fringe) -> tuple:
        hunt_cell = None
        min_dist = float('inf')
        start_x, start_y = self.entry
        for item in fringe:
            nx, ny, distance, parent = item
            dist = abs(nx - start_x) + abs(ny - start_y)
            if dist < min_dist:
                min_dist = min
                hunt_cell = item
        return hunt_cell

    def generate(self) -> Any:
        start = self.entry
        fringe = []
        hunt = False

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
            if hunt == True:
                target = self.hunt(fringe)
                fringe.remove(target)
                nx, ny, direction, current = target
            else:
                nx, ny, direction, current = fringe.pop()
                hunt = False

            if (nx, ny) in self.visited:
                continue

            self.remove_wall(current, direction)
            self.visited.add((nx, ny))
            self.solution[(nx, ny)] = current

            neighbors = self.get_neighbors((nx, ny))
            random.shuffle(neighbors)

            if len(neighbors) == 0:
                hunt = True
                continue

            for nnx, nny, new_direction in neighbors:
                possible_moves = []
                if (nnx, nny) not in self.visited:
                    possible_moves.append((nnx, nny, new_direction, (nx, ny)))

                random.shuffle(possible_moves)
                for move in possible_moves:
                    fringe.append(move)

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

        if self.perfect is False:
            self.create_loops()
