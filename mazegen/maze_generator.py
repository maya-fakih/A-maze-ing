from typing import Any, List, Tuple
from abc import ABC, abstractmethod
import sys


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
        self.width = settings_dict.get("width")
        self.height = settings_dict.get("height")
        self.entry = settings_dict.get("entry")
        self.exit = settings_dict.get("exit")
        self.output_file = settings_dict.get("output_file", "output_maze.txt")
        self.perfect = settings_dict.get("perfect", "false")
        self.wall_color = settings_dict.get("wall_color", "white")
        self.flag_color = settings_dict.get("flag_color", "blue")
        self.algorithm = settings_dict.get("algorithm", "dfs")
        self.shape = settings_dict.get("shape", "square")
        self.maze = (
            [[0 for _ in range(self.height)] for _ in range(self.width)]
        )
        self.logo_cells = set()
        self.solution = {}
        self.visited = set()
        self.path = []

    @abstractmethod
    def generate(self) -> Any:
        pass

    @abstractmethod
    def initialize_maze(self) -> None:
        pass

    @abstractmethod
    def create_loops(self) -> None:
        pass

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
