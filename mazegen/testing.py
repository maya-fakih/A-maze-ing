from default_generator import BasicGenerator


config = {
    "width": 25,
    "height": 20,
    "entry": (0, 0),
    "exit": (18, 19),
    "output_file": "test.txt",
    "perfect": True,
    "wall_color": "cyan",
    "flag_color": "blue",
    "algorithm": "dfs",
    "shape": "square"
}


generator = BasicGenerator(config)
generator.generate()
generator.display_maze()
