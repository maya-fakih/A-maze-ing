from default_generator import BasicGenerator



config = {
    "width": 25,
    "height": 20,
    "entry": (0, 0),
    "exit": (18, 19),
    "output_file": "test.txt",
    "perfect": True,
    "wall_color": "white",
    "flag_color": "blue",
    "algorithm": "dfs",
    "shape": "square"
}

def print_maze(self):
    """Print the maze grid as binary values"""
    for y in range(self.height):
        row = []
        for x in range(self.width):
            row.append(f"{self.maze[x][y]:04b}")
        print(" ".join(row))

generator = BasicGenerator(config)
generator.generate()
generator.display_ascii()
print(f" the generator is perfect flag is: {generator.perfect}")

