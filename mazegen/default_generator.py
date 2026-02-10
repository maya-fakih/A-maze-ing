from typing import Any, List, Dict
from maze_generator import MazeGenerator
from collections import deque
import random


class BasicGenerator(MazeGenerator):
    """Prim's algorithm"""

    def __init__(self, settings_dict):
        super().__init__(settings_dict)

    def generate(self) -> Any:
        pass
