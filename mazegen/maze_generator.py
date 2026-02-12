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

    def display_maze(self):
        H = self.height
        W = self.width
        maze = self.maze
        SOUTH = 2
        EAST = 4

        # Map color names to ANSI codes
        color_map = {
            "black": 30,
            "red": 31,
            "green": 32,
            "yellow": 33,
            "blue": 34,
            "magenta": 35,
            "cyan": 36,
            "white": 37,
            "bright_black": 90,
            "bright_red": 91,
            "bright_green": 92,
            "bright_yellow": 93,
            "bright_blue": 94,
            "bright_magenta": 95,
            "bright_cyan": 96,
            "bright_white": 97,

            "grey": 90,
            "gray": 90,
            "light_red": 91,
            "light_green": 92,
            "light_yellow": 93,
            "light_blue": 94,
            "light_magenta": 95,
            "light_cyan": 96,
            "light_white": 97,
        }

        # default white
        wall_code = f"\033[{color_map.get(self.wall_color, 37)}m"
        reset_code = "\033[0m"

        entry_r, entry_c = self.entry
        exit_r, exit_c = self.exit

        for r in range(2 * H + 1):
            for c in range(2 * W + 1):
                # Corners
                if r % 2 == 0 and c % 2 == 0:
                    print(wall_code + "+" + reset_code, end="")

                # Horizontal walls
                elif r % 2 == 0 and c % 2 == 1:
                    if r == 0 or r == 2 * H:
                        print(wall_code + "---" + reset_code, end="")
                    else:
                        cell_row = r // 2 - 1
                        cell_col = c // 2
                        if maze[cell_col][cell_row] & SOUTH:
                            print(wall_code + "---" + reset_code, end="")
                        else:
                            print("   ", end="")

                # Vertical walls
                elif r % 2 == 1 and c % 2 == 0:
                    if c == 0 or c == 2 * W:
                        print(wall_code + "|" + reset_code, end="")
                    else:
                        cell_row = r // 2
                        cell_col = c // 2 - 1
                        if maze[cell_col][cell_row] & EAST:
                            print(wall_code + "|" + reset_code, end="")
                        else:
                            print(" ", end="")

                # Cell interior
                else:
                    cell_row = r // 2
                    cell_col = c // 2
                    if (cell_row, cell_col) == (entry_r, entry_c):
                        print(" E ", end="")  # Entry
                    elif (cell_row, cell_col) == (exit_r, exit_c):
                        print(" X ", end="")  # Exit
                    else:
                        print("   ", end="")

            print()

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
