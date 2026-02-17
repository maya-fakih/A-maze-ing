from .maze_solver import MazeSolver

class BFSSolver(MazeSolver):
    """Breadth-First Search Agent"""

    from ..generators import MazeGenerator
    def solve(self, maze: MazeGenerator) -> list:
        start = maze.entry
        goal = maze.exit

        visited = set()
        fringe = [(start, [start], [])]
        while fringe:
            current_cell, path, dir = fringe.pop(0)

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