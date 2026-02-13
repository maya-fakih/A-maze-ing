from typing import Any, List, Tuple
from abc import ABC, abstractmethod


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

    def __init__(self, settings_dict: dict):
        self.settings_dict = settings_dict
        self.width = settings_dict.get("width")
        self.height = settings_dict.get("height")
        self.entry = settings_dict.get("entry")
        self.exit = settings_dict.get("exit")
        self.output_file = settings_dict.get("output_file", "output_maze.txt")
        self.perfect = settings_dict.get("perfect", "false")
        self.wall_color = settings_dict.get("wall_color", "white")
        self.flag_color = settings_dict.get("flag_color", "blue")
        self.generation_algorithm = settings_dict.get(
            "generation_algorithm", "dfs")
        self.solver_algorithm = settings_dict.get(
            "solver_algorithm", "dfs"
        )
        self.shape = settings_dict.get("shape", "square")
        self.maze = (
            [[0 for _ in range(self.height)] for _ in range(self.width)]
        )
        self.logo_cells = set()
        self.solution = {}
        self.visited = set()
        self.path = []

    # instantiate correct subclass based on settings -> factory method
    def create(self):
        # Local imports avoid circular dependencies with subclasses
        # generation_algorithm
        from .perfect_generator import PerfectGenerator
        from .default_generator import BasicGenerator
        from .shape_generator import ShapeGenerator
        match self.generation_algorithm:
            case "prim":
                return BasicGenerator(self.settings_dict)
            case "dfs":
                #
            case "bfs":
                #
            
            case "huntkill":
                #

    @abstractmethod
    def generate(self) -> Any:
        pass

    @abstractmethod
    def initialize_maze(self) -> None:
        pass

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

    def write_to_file(self) -> None:
        pass
