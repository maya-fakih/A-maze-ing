from .maze_solver import MazeSolver
from ..generators.maze_generator import MazeGenerator

class DFSolver(MazeSolver):
    """Depth-First Search Agent"""

    def solve(self) -> list:
        start = self.maze.entry
        goal = self.maze.exit

        visited = set()
        fringe = [(start, [start], [])]
        while fringe:
            current_cell, path, dir = fringe.pop()

            if current_cell in visited:
                continue

            visited.add(current_cell)

            if current_cell == goal:
                self.solution_cells = path
                return dir

            for nx, ny, d in self.reachable_neighbors(current_cell):
                neighbor = (nx, ny)
                if neighbor not in visited:
                    fringe.append((neighbor, path + [neighbor], dir + [d]))
        return []