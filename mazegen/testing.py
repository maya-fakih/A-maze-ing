from default_generator import BasicGenerator



config = {
    "width": 20,
    "height": 20,
    "entry": (0, 0),
    "exit": (15, 15),
    "output_file": "test.txt",
    "perfect": "false",
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

print(f"path length: {len(generator.path)}")

generator.display_ascii()


