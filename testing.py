from mazegen.generators.prim_generator import PrimGenerator
from mazegen.generators.dfs_generator import DFSGenerator
from mazegen.generators.bfs_generator import BFSGenerator
from mazegen.generators.huntkill_generator import HuntKillGenerator


config = {
    "width": 25,
    "height": 20,
    "entry": (0, 0),
    "exit": (18, 19),
    "output_file": "test.txt",
    "perfect": False,
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
