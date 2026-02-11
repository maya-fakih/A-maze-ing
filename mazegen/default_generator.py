from typing import Any, List, Dict, Tuple
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
    

    def generate(self) -> Any:
        reached_goal = False
        self.path.extend(self.logo_cells)
        self.initialize_maze()
        

