from typing import Any, List, Dict
from abc import ABC, abstractmethod


class MazeGenerator(ABC):
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
        self.maze = List[List[int]]

    # add function to initialize all sides closed
    # add function to draw the 42 logo (should print error message if it cant print 42 logo w continues normally)

    @abstractmethod
    def generate(self) -> Any:
        # the str is the order of the cells it creates in order
        # so we can animate it later
        pass

    def write_to_file(self) -> None:
        pass
