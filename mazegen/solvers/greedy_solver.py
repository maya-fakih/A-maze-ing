from .maze_solver import MazeSolver
import heapq


class GreedySolver(MazeSolver):
    """Greedy Search Agent"""

    def priority(self, cell: tuple) -> int:
        """Handle priority."""
        return self.huristic(cell)

    def solve(self) -> list:
        """Solve the value."""
        start = self.maze.entry
        goal = self.maze.exit
        self.animation_path = []
        self.animation_path.append((start, True))

        visited = set()
        fringe = [(0, (start, [start], []))]
        while fringe:
            _, (current_cell, path, dir) = heapq.heappop(fringe)

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
                n = (nx, ny)
                if n not in visited:
                    item = (self.priority(n), (n, path + [n], dir + [d]))
                    heapq.heappush(fringe, item)
        return []
