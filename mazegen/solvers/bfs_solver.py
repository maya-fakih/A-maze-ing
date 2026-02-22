from .maze_solver import MazeSolver


class BFSolver(MazeSolver):
    """Breadth-First Search Agent"""

    def solve(self) -> list:
        """Solve the value."""
        start = self.maze.entry
        goal = self.maze.exit
        self.animation_path = []
        self.animation_path.append((start, True))

        visited = set()
        fringe = [(start, [start], [])]
        while fringe:
            current_cell, path, dir = fringe.pop(0)

            if current_cell in visited:
                continue

            visited.add(current_cell)
            self.animation_path.append((current_cell, False))

            if current_cell == goal:
                self.solution_cells = path
                for i in range(len(self.animation_path)):
                    cell, _ = self.animation_path[i]
                    if cell in self.solution_cells:
                        self.animation_path[i] = (cell, True)
                return dir

            for nx, ny, d in self.reachable_neighbors(current_cell):
                neighbor = (nx, ny)
                if neighbor not in visited:
                    fringe.append((neighbor, path + [neighbor], dir + [d]))
        return []
