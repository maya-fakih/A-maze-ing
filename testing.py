from mazegen.generators import BFSGenerator, DFSGenerator
from mazegen.generators import PrimGenerator, HuntKillGenerator


config = {
    "width": 30,
    "height": 30,
    "entry": (8, 8),
    "exit": (18, 19),
    "output_file": "test.txt",
    "perfect": True,
    "wall_color": "white",
    "flag_color": "blue",
    "algorithm": "dfs",
    "shape": "star"
}


def print_maze(self):
    """Print the maze grid as binary values"""
    for y in range(self.height):
        row = []
        for x in range(self.width):
            row.append(f"{self.maze[x][y]:04b}")
        print(" ".join(row))


print("\n")

print("Prims Generator")

generator = PrimGenerator(config)
generator.generate()
generator.display_ascii()
print(f" the generator is perfect flag is: {generator.perfect}")


print("\n")

print("BFS Generator")

generator = BFSGenerator(config)
generator.generate()
generator.display_ascii()
print(f" the generator is perfect flag is: {generator.perfect}")

print("DFS Generator")
generator = DFSGenerator(config)
generator.generate()
generator.display_ascii()
print(f" the generator is perfect flag is: {generator.perfect}")


print("Hunt and Kill Generator")
generator = HuntKillGenerator(config)
generator.generate()
generator.display_ascii()
print(f" the generator is perfect flag is: {generator.perfect}")
