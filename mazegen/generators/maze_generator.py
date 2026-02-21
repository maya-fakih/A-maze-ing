from ..shapes import Star, Heart, Flower
from ..errors import InitializationError
from typing import Any, List, Tuple
from abc import ABC, abstractmethod
import sys
import random
import os


class MazeGenerator(ABC):
    NORTH = 0b0001
    EAST = 0b0010
    SOUTH = 0b0100
    WEST = 0b1000

    MASK = {
        'N': NORTH,
        'E': EAST,
        'S': SOUTH,
        'W': WEST
    }

    WALLS = ['N', 'E', 'W', 'S']

    OPPOSITE = {
        NORTH: SOUTH,
        SOUTH: NORTH,
        EAST: WEST,
        WEST: EAST
    }

    # instantiate correct subclass based on settings -> factory method

    @classmethod
    def create_generator(cls, settings: dict):
        from .prim_generator import PrimGenerator
        from .dfs_generator import DFSGenerator
        from .bfs_generator import BFSGenerator
        from .huntkill_generator import HuntKillGenerator
        match settings["generation_algorithm"]:
            case "prim":
                return PrimGenerator(settings)
            case "dfs":
                return DFSGenerator(settings)
            case "bfs":
                return BFSGenerator(settings)
            case "huntkill":
                return HuntKillGenerator(settings)

    def __init__(self, settings_dict: dict):
        self.settings = settings_dict
        self.width = settings_dict.get("width")
        self.height = settings_dict.get("height")
        self.entry = settings_dict.get("entry")
        self.exit = settings_dict.get("exit")
        self.output_file = settings_dict.get("output_file",
                                             "output/output_maze.txt")
        self.perfect = settings_dict.get("perfect", False)
        self.wall_color = settings_dict.get("wall_color", "white")
        self.flag_color = settings_dict.get("flag_color", "blue")
        self.path_color = settings_dict.get("path_color")
        self.generation_algorithm = settings_dict.get(
            "generation_algorithm", "dfs")
        self.solver_algorithm = settings_dict.get(
            "solver_algorithm", "dfs"
        )
        self.display_mode = settings_dict.get(
            "display_mode", "ascii"
        )
        self.shape = settings_dict.get("shape", "square")
        self.maze = (
            [[0 for _ in range(self.height)] for _ in range(self.width)]
        )
        self.logo_cells = set()
        self._add_42_logo()
        self.validate_entry_exit()
        self.solution = []
        self.visited = set()
        self.path = []
        self.generation_path = []

    @abstractmethod
    def generate(self) -> Any:
        pass

    def validate_entry_exit(self) -> None:
        if self.entry in self.logo_cells:
            raise InitializationError("Entry point cannot be on the logo.")
        if self.exit in self.logo_cells:
            raise InitializationError("Exit point cannot be on the logo.")
        if self.shape != "square":
            self.flood_fill_shape(self.entry)
            self.flood_fill_shape(self.exit)

    def flood_fill_shape(self, start: Tuple) -> None:
        h = self.height
        w = self.width
        to_process = [start]
        processed = set([start])

        while to_process:
            current_x, current_y = to_process.pop(0)
            neighbors = self.get_neighbors((current_x, current_y))

            for nx, ny, _ in neighbors:
                if nx == 0 or nx == w - 1 or ny == 0 or ny == h - 1:
                    s = "Shape border cannot be on the edge of the maze."
                    raise InitializationError(s)
                neighbor = (nx, ny)
                if neighbor not in processed:
                    processed.add(neighbor)
                    to_process.append(neighbor)

    def initialize_maze(self) -> None:
        self.path.clear()
        self.generation_path.clear()
        self.visited.clear()
        self.solution.clear()
        for x in range(self.width):
            for y in range(self.height):
                if (x, y) not in self.logo_cells:
                    self.maze[x][y] = 15

        if self.shape != "square":
            self.remove_walls_outside_shape()

    def find_solution_path(self) -> None:
        from ..solvers.astar_solver import AStarSolver
        from ..solvers.bfs_solver import BFSolver
        # from ..solvers.dfs_solver import DFSolver
        from ..solvers.ucs_solver import UCSolver

        solver_map = {
            "bfs": BFSolver,
            "a*": AStarSolver,
            "ucs": UCSolver,
        }
        solver_class = solver_map.get(self.solver_algorithm, BFSolver)
        solver = solver_class(self)
        self.solution = solver.solve()
        print(f"solution path: {self.solution}")

        self.path = []
        for cell in self.visited:
            x, y = cell
            if cell == self.entry:
                self.path.append((cell, self.maze[x][y], True))
            elif cell in solver.solution_cells:
                self.path.append((cell, self.maze[x][y], True))
            else:
                self.path.append((cell, self.maze[x][y], False))

    def remove_walls_outside_shape(self) -> None:
        start = (0, 0)
        end = (self.width - 1, self.height - 1)
        corner = (self.width - 1, 0)
        corner2 = (0, self.height - 1)
        to_process = [start, end, corner, corner2]
        processed = set([start])

        while to_process:
            current_x, current_y = to_process.pop(0)
            neighbors = self.get_neighbors((current_x, current_y))

            for nx, ny, direction in neighbors:
                neighbor = (nx, ny)
                self.remove_wall((current_x, current_y), direction)
                if neighbor not in processed:
                    processed.add(neighbor)
                    to_process.append(neighbor)

    def create_loops(self) -> None:
        path_base = {c for c, _, s in self.path}

        path = list(path_base)
        random.shuffle(path)

        for i in range(0, (len(path)), 2):
            current = path[i]

            if current in self.logo_cells:
                continue

            neighbors = self.get_neighbors(current)
            random.shuffle(neighbors)

            for nx, ny, direction in neighbors:
                if (nx, ny) in self.logo_cells:
                    continue
                else:
                    self.remove_wall(current, direction)
                    break

    def has_wall(self, location: Tuple, direction: str) -> bool:
        x, y = location

        if direction == 'W' and x == 0:
            return False
        if direction == 'E' and x == self.width-1:
            return False
        if direction == 'N' and y == 0:
            return False
        if direction == 'S' and y == self.height-1:
            return False

        if direction == 'N':
            nx, ny = x, y-1
        elif direction == 'S':
            nx, ny = x, y+1
        elif direction == 'E':
            nx, ny = x+1, y
        elif direction == 'W':
            nx, ny = x-1, y

        if (x, y) in self.logo_cells or (nx, ny) in self.logo_cells:
            return False

        cell_value = self.maze[x][y]
        mask = self.MASK[direction]
        return (cell_value & mask) != 0

    def remove_wall(self, cell: Tuple, direction: str) -> None:
        x, y = cell

        if direction == 'N':
            nx, ny = x, y-1
        elif direction == 'S':
            nx, ny = x, y+1
        elif direction == 'E':
            nx, ny = x+1, y
        elif direction == 'W':
            nx, ny = x-1, y

        mask = self.MASK[direction]
        opposite_mask = self.OPPOSITE[mask]

        self.maze[x][y] &= ~mask
        self.maze[nx][ny] &= ~opposite_mask

    def get_neighbors(self, cell: Tuple) -> List[Tuple]:
        x, y = cell
        possible = [
            (x+1, y, 'E'),
            (x-1, y, 'W'),
            (x, y+1, 'S'),
            (x, y-1, 'N')
        ]
        neighbors = []
        for nx, ny, direction in possible:
            if 0 <= nx < self.width and 0 <= ny < self.height:
                if (nx, ny) not in self.logo_cells:
                    neighbors.append((nx, ny, direction))
        return neighbors

    def _add_42_logo(self):
        """Create 42 logo pattern in the maze if dimensions allow it."""
        if self.width < 10 or self.height < 10:
            sys.stderr.write("Could not draw 42 logo. (dimentions too small)")
            return

        start_x = self.width // 2 - 4
        start_y = self.height // 2 - 2
        logos = [
            (start_x, start_y),
            (start_x, start_y + 1),
            (start_x, start_y + 2),
            (start_x + 1, start_y + 2),
            (start_x + 2, start_y + 2),
            (start_x + 2, start_y + 3),
            (start_x + 2, start_y + 4),
            (start_x + 4, start_y),
            (start_x + 4, start_y + 2),
            (start_x + 4, start_y + 3),
            (start_x + 4, start_y + 4),
            (start_x + 5, start_y),
            (start_x + 5, start_y + 2),
            (start_x + 5, start_y + 4),
            (start_x + 6, start_y),
            (start_x + 6, start_y + 1),
            (start_x + 6, start_y + 2),
            (start_x + 6, start_y + 4),
        ]
        for cell in logos:
            self.logo_cells.add(cell)

        if self.shape != "square":
            border = self.add_shape_border()
            for cell in border:
                self.logo_cells.add(cell)

        for x, y in self.logo_cells:
            if 0 <= x < self.width and 0 <= y < self.height:
                self.maze[x][y] = 15

    def add_shape_border(self) -> list:
        if self.shape == "star":
            shape = Star(self.width, self.height)
        elif self.shape == "heart":
            shape = Heart(self.width, self.height)
        elif self.shape == "flower":
            shape = Flower(self.width, self.height)
        return (shape.generate())

    def output_to_file(self) -> None:
        output_dir = os.path.dirname(self.output_file)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        with open(self.output_file, "w", encoding="utf-8") as f:
            for r in range(self.height):
                for c in range(self.width):
                    f.write(f"{format(self.maze[c][r], 'X')}")
                f.write("\n")
            f.write("\n")
            f.write(f"{self.entry[0]},{self.entry[1]}")
            f.write("\n")
            f.write(f"{self.exit[0]},{self.exit[1]}")
            f.write("\n")
            f.write(f"{''.join(self.solution)}")

    def write_path(self, path: str) -> None:
        # write ordered generation steps for minilibx animation
        path_dir = os.path.dirname(path)
        if path_dir:
            os.makedirs(path_dir, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            for cell in self.generation_path:
                for x in cell[0]:
                    f.write(f"{x} ")
                f.write(f"{cell[1]} ")
                f.write(f"{cell[2]}\n")

    def write_logo_cells(self, path: str) -> None:
        logo_dir = os.path.dirname(path)
        if logo_dir:
            os.makedirs(logo_dir, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            for x, y in sorted(self.logo_cells):
                f.write(f"{x} {y}\n")
