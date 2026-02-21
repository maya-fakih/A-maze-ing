from .maze_solver import MazeSolver


class DFSolver(MazeSolver):
    """Depth-First Search Agent"""

    def solve(self) -> list:
        start = self.maze.entry
        goal = self.maze.exit
        self.animation_path = []
        self.animation_path.append((start, True))

        visited = set()
        fringe = [(start, [start], [])]
        while fringe:
            current_cell, path, dir = fringe.pop()

            if current_cell in visited:
                continue

            visited.add(current_cell)
            self.animation_path.append((current_cell, False))

            if current_cell == goal:
                self.solution_cells = path
<<<<<<< HEAD
                updated_path = []
                for cell, sol in self.path:
                    if cell in self.solution_cells:
                        updated_path.append((cell, True))
                    else:
                        updated_path.append((cell, False))
                self.path = updated_path
=======
                for i in range(len(self.animation_path)):
                    cell, _ = self.animation_path[i]
                    if cell in self.solution_cells:
                        self.animation_path[i] = (cell, True)
>>>>>>> 900e994780fbab17d50e15bd6194167980821dd1
                return dir

            for nx, ny, d in self.reachable_neighbors(current_cell):
                neighbor = (nx, ny)
                if neighbor not in visited:
                    fringe.append((neighbor, path + [neighbor], dir + [d]))
        return []
