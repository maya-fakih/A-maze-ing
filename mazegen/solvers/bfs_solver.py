from .maze_solver import MazeSolver


class BFSolver(MazeSolver):
    """Breadth-First Search Agent"""

    def solve(self) -> list:
        start = self.maze.entry
        goal = self.maze.exit
        self.path = []
        self.path.append((start, True))

        visited = set()
        fringe = [(start, [start], [])]
        while fringe:
            current_cell, path, dir = fringe.pop(0)

            if current_cell in visited:
                continue

            visited.add(current_cell)
            self.path.append((current_cell, False))

            if current_cell == goal:
                self.solution_cells = path
                for cell, sol in self.path:
                    if cell in self.solution_cells:
                        self.solution.append((cell, True))
                    else:
                        self.solution.append((cell, False))
                return dir

            for nx, ny, d in self.reachable_neighbors(current_cell):
                neighbor = (nx, ny)
                if neighbor not in visited:
                    fringe.append((neighbor, path + [neighbor], dir + [d]))
        return []
