from ..shapes import Star, Heart, Flower
from ..errors import InitializationError
from typing import Any, List, Tuple, Set, Optional
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

    @classmethod
    def create_generator(cls, settings: dict[str, Any]) -> "MazeGenerator":
        """Instantiate generator matching selected algorithm. Args: cls generator base class, settings validated settings map. Returns: Concrete maze generator instance."""
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
            case _:
                return PrimGenerator(settings)

    def __init__(self, settings_dict: dict[str, Any]) -> None:
        """Initialize common maze generation state. Args: settings_dict validated configuration values. Returns: None."""
        self.settings = settings_dict

        # Validate required fields
        width_val = settings_dict.get("width")
        height_val = settings_dict.get("height")
        entry_val = settings_dict.get("entry")
        exit_val = settings_dict.get("exit")

        if width_val is None or height_val is None:
            raise InitializationError("Width and height must be provided")
        if entry_val is None or exit_val is None:
            raise InitializationError("Entry and exit must be provided")

        self.width: int = int(width_val)
        self.height: int = int(height_val)
        self.entry: Tuple[int, int] = tuple(entry_val)
        self.exit: Tuple[int, int] = tuple(exit_val)
        out = "output/output_maze.txt"
        self.output_file: str = settings_dict.get("output_file", out)
        self.perfect: bool = settings_dict.get("perfect", False)
        self.wall_color: str = settings_dict.get("wall_color", "white")
        self.flag_color: str = settings_dict.get("flag_color", "blue")
        self.path_color: Optional[str] = settings_dict.get("path_color")
        alg = "generation_algorithm"
        self.generation_algorithm: str = settings_dict.get(alg, "dfs")
        solver = "solver_algorithm"
        self.solver_algorithm: str = settings_dict.get(solver, "dfs")
        self.display_mode: str = settings_dict.get("display_mode", "ascii")
        self.shape: str = settings_dict.get("shape", "square")

        if self.shape != "square" and (self.width < 20 or self.height < 20):
            s = "Minimum dimensions required: 20x20."
            raise InitializationError(
                f"Maze dimensions too small for shape '{self.shape}'.\n"
                f"{s} Current: {self.width}x{self.height}"
            )
        h = range(self.height)
        w = range(self.width)
        self.maze: List[List[int]] = [[0 for _ in h] for _ in w]
        self.logo_cells: Set[Tuple[int, int]] = set()
        self.solution: List[str] = []
        self.visited: Set[Tuple[int, int]] = set()
        self.generation_path: List[Tuple[Tuple[int, int], int, bool]] = []

        self.add_42_logo()
        self.validate_entry_exit()

    @abstractmethod
    def generate(self) -> None:
        """Generate maze structure and solution data. Args: self generator instance. Returns: None."""
        raise NotImplementedError

    def validate_entry_exit(self) -> None:
        """Validate entry/exit positions against constraints. Args: self generator instance. Returns: None."""
        if self.entry in self.logo_cells:
            raise InitializationError("Entry point cannot be on the logo.")
        if self.exit in self.logo_cells:
            raise InitializationError("Exit point cannot be on the logo.")
        if self.shape != "square":
            self.flood_fill_shape(self.entry)
            self.flood_fill_shape(self.exit)

    def flood_fill_shape(self, start: Tuple[int, int]) -> None:
        """Flood-fill shape interior from a start cell. Args: start seed coordinate to test connectivity. Returns: None."""
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

    def reset_maze(self) -> None:
        """Reset maze grid walls and animation state. Args: self generator instance. Returns: None."""
        for x in range(self.width):
            for y in range(self.height):
                if (x, y) not in self.logo_cells:
                    self.maze[x][y] = 15
        if self.shape != "square":
            self.remove_walls_outside_shape()
        for cell in self.logo_cells:
            x, y = cell
            self.generation_path.append((cell, self.maze[x][y], False))

    def initialize_maze(self) -> None:
        """Prepare maze for a fresh generation pass. Args: self generator instance. Returns: None."""
        self.generation_path.clear()
        self.visited = set(self.logo_cells)
        self.solution.clear()
        self.reset_maze()

    def find_solution_path(self) -> None:
        """Run configured solver and mark solution cells. Args: self generator instance. Returns: None."""
        from ..solvers.astar_solver import AStarSolver
        from ..solvers.bfs_solver import BFSolver
        from ..solvers.ucs_solver import UCSolver

        solver_map = {
            "bfs": BFSolver,
            "a*": AStarSolver,
            "ucs": UCSolver,
        }
        solver_class = solver_map.get(self.solver_algorithm, BFSolver)
        solver = solver_class(self)
        self.solution = solver.solve()

        for i in range(len(self.generation_path)):
            cell, _, _ = self.generation_path[i]
            x, y = cell
            if cell == self.entry:
                self.generation_path[i] = (cell, self.maze[x][y], True)
            elif cell in solver.solution_cells:
                self.generation_path[i] = (cell, self.maze[x][y], True)
            else:
                self.generation_path[i] = (cell, self.maze[x][y], False)

    def remove_walls_outside_shape(self) -> None:
        """Open cells outside non-square shape boundary. Args: self generator instance. Returns: None."""
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
                self.remove_wall((current_x, current_y), direction, False)
                self.visited.add(neighbor)
                if neighbor not in processed:
                    processed.add(neighbor)
                    to_process.append(neighbor)

    def create_loops(self) -> None:
        """Add extra openings to make maze imperfect. Args: self generator instance. Returns: None."""
        path_base = {c for c, _, _ in self.generation_path}

        path = list(path_base)
        random.shuffle(path)

        for i in range(0, len(path), 2):
            current = path[i]

            if current in self.logo_cells:
                continue

            neighbors = self.get_neighbors(current)
            random.shuffle(neighbors)

            for nx, ny, direction in neighbors:
                if (nx, ny) in self.logo_cells:
                    continue
                else:
                    self.remove_wall(current, direction, True)
                    break

    def has_wall(self, location: Tuple[int, int], direction: str) -> bool:
        """Check if a wall exists in a direction. Args: location source cell, direction wall direction token. Returns: True when wall is present."""
        x, y = location

        if direction == 'W' and x == 0:
            return False
        if direction == 'E' and x == self.width - 1:
            return False
        if direction == 'N' and y == 0:
            return False
        if direction == 'S' and y == self.height - 1:
            return False

        if direction == 'N':
            nx, ny = x, y - 1
        elif direction == 'S':
            nx, ny = x, y + 1
        elif direction == 'E':
            nx, ny = x + 1, y
        elif direction == 'W':
            nx, ny = x - 1, y

        if (x, y) in self.logo_cells or (nx, ny) in self.logo_cells:
            return False

        cell_value = self.maze[x][y]
        mask = self.MASK[direction]
        return (cell_value & mask) != 0

    def remove_wall(self, cell: Tuple[int, int], dir: str, a: bool) -> None:
        """Remove wall between adjacent cells. Args: cell source cell, dir direction to carve, a whether to record animation step. Returns: None."""
        x, y = cell

        if dir == 'N':
            nx, ny = x, y - 1
        elif dir == 'S':
            nx, ny = x, y + 1
        elif dir == 'E':
            nx, ny = x + 1, y
        elif dir == 'W':
            nx, ny = x - 1, y

        mask = self.MASK[dir]
        opposite_mask = self.OPPOSITE[mask]

        self.maze[x][y] &= ~mask
        self.maze[nx][ny] &= ~opposite_mask
        if a:
            self.generation_path.append(((x, y), self.maze[x][y], False))
            self.generation_path.append(((nx, ny), self.maze[nx][ny], False))

    def get_neighbors(self, c: Tuple[int, int]) -> List[Tuple[int, int, str]]:
        """List valid neighboring cells with directions. Args: c origin cell coordinates. Returns: Neighbor tuples of x, y, direction."""
        x, y = c
        possible = [
            (x + 1, y, 'E'),
            (x - 1, y, 'W'),
            (x, y + 1, 'S'),
            (x, y - 1, 'N')
        ]
        neighbors = []
        for nx, ny, direction in possible:
            if 0 <= nx < self.width and 0 <= ny < self.height:
                if (nx, ny) not in self.logo_cells:
                    neighbors.append((nx, ny, direction))
        return neighbors

    def add_42_logo(self) -> None:
        """Reserve maze cells forming the 42 logo. Args: self generator instance. Returns: None."""
        if self.width < 10 or self.height < 10:
            sys.stdout.flush()
            sys.stderr.write("Could not draw 42 logo. (dimentions too small)\n")
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

    def add_shape_border(self) -> List[Tuple[int, int]]:
        """Generate border coordinates for configured shape. Args: self generator instance. Returns: Shape border cell list."""
        if self.shape == "star":
            return Star(self.width, self.height).generate()
        elif self.shape == "heart":
            return Heart(self.width, self.height).generate()
        elif self.shape == "flower":
            return Flower(self.width, self.height).generate()
        else:
            return []

    def output_to_file(self) -> None:
        """Write maze grid and metadata to output file. Args: self generator instance. Returns: None."""
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
        """Write generation animation path to file. Args: path destination file path. Returns: None."""
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
        """Write reserved logo cell coordinates to file. Args: path destination file path. Returns: None."""
        logo_dir = os.path.dirname(path)
        if logo_dir:
            os.makedirs(logo_dir, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            for x, y in sorted(self.logo_cells):
                f.write(f"{x} {y}\n")
