from .maze_generator import MazeGenerator


class PerfectGenerator(MazeGenerator):
    def __init__(self, settings_dict):
        super().__init__(settings_dict)

    def generate(self):
        """Wilson's algorithm"""
        return super().generate()
