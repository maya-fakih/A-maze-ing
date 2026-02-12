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
        self.output_file = settings_dict.get("output_file")
        self.perfect = settings_dict.get("perfect")
        self.wall_color = settings_dict.get("wall_color", "white")
        self.flag_color = settings_dict.get("flag_color", "blue")
        self.algorithm = settings_dict.get("algorithm", "dfs")
        self.shape = settings_dict.get("shape", "square")
        self.maze = (
            [[0 for _ in range(self.height)] for _ in range(self.width)]
        )
        self.logo_cells = set()
        self._add_42_logo()
        self.solution = {}
        self.visited = set()
        self.path = []
    
    @abstractmethod
    def generate(self) -> Any:
        pass

    @abstractmethod
    def initialize_maze(self) -> None:
        pass

    def display_ascii(self):
        """Display maze as ASCII art"""
        for y in range(self.height):
            top_row = ""
            mid_row = ""
            for x in range(self.width):
                cell = self.maze[x][y]
                
                is_logo = (x,y) in self.logo_cells

                if y == 0 or (cell & self.NORTH):
                    top_row += "+---"
                else:
                    top_row += "+   "
                
                if (x,y) == self.entry:
                    mid_row += "| S "
                elif (x, y) == self.exit:
                    mid_row += "  E "
                elif( x == 0 or (cell & self.WEST)) and is_logo:
                    mid_row += "|###"
                elif x == 0 or (cell & self.WEST):
                    mid_row += "|   "
                else:
                    mid_row += "    "
            
            print(top_row + "+")
            print(mid_row + "|")
        
        print("+---" * self.width + "+")
    

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

        self.logo_cells.add((start_x, start_y))
        self.logo_cells.add((start_x, start_y + 1))
        self.logo_cells.add((start_x, start_y + 2))

        self.logo_cells.add((start_x + 1, start_y + 2))

        self.logo_cells.add((start_x + 2, start_y + 2))
        self.logo_cells.add((start_x + 2, start_y + 3))
        self.logo_cells.add((start_x + 2, start_y + 4))

        self.logo_cells.add((start_x + 4, start_y))
        self.logo_cells.add((start_x + 4, start_y + 2))
        self.logo_cells.add((start_x + 4, start_y + 3))
        self.logo_cells.add((start_x + 4, start_y + 4))

        self.logo_cells.add((start_x + 5, start_y))
        self.logo_cells.add((start_x + 5, start_y + 2))
        self.logo_cells.add((start_x + 5, start_y + 4))

        self.logo_cells.add((start_x + 6, start_y))
        self.logo_cells.add((start_x + 6, start_y + 1))
        self.logo_cells.add((start_x + 6, start_y + 2))
        self.logo_cells.add((start_x + 6, start_y + 4))

        for x, y in self.logo_cells:
            if 0 <= x < self.width and 0 <= y < self.height:
                self.maze[x][y] = 15

    def write_to_file(self) -> None:
        pass
