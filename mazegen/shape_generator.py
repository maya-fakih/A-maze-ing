from .maze_generator import MazeGenerator


class ShapeGenerator(MazeGenerator):
    def __init__(self, settings_dict):
        super().__init__(settings_dict)

    def generate(self):
        """CSP algorithm"""
        return super().generate()
