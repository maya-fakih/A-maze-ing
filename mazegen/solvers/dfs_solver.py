from .maze_solver import MazeSolver


class DFSolver(MazeSolver):
    """Depth-First Search Agent"""

    def solve(self) -> list:
        start = self.maze.entry
        goal = self.maze.exit
        self.path = []
        self.path.append((start, True))

        visited = set()
        fringe = [(start, [start], [])]
        while fringe:
            current_cell, path, dir = fringe.pop()

            if current_cell in visited:
                continue

            visited.add(current_cell)
            self.path.append((current_cell, False))

            if current_cell == goal:
                self.solution_cells = path
                updated_path = []
                for cell, sol in self.path:
                    if cell in self.solution_cells:
                        updated_path.append((cell, True))
                    else:
                        updated_path.append((cell, False))
                self.path = updated_path
                return dir

            for nx, ny, d in self.reachable_neighbors(current_cell):
                neighbor = (nx, ny)
                if neighbor not in visited:
                    fringe.append((neighbor, path + [neighbor], dir + [d]))
        return []
