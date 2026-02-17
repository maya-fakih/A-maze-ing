from .maze_solver import MazeSolver
import heapq


class GreedySolver(MazeSolver):
    """Greedy Search Agent"""

    def priority(self, cell: tuple) -> int:
        """Priority function for Greedy Search (heuristic only)"""
        return self.huristic(cell)

    def solve(self) -> list:
        start = self.maze.entry
        goal = self.maze.exit
        self.path = []
        self.path.append((start, True))

        visited = set()
        fringe = [(0, (start, [start], []))]
        while fringe:
            _, (current_cell, path, dir) = heapq.heappop(fringe)

            if current_cell in visited:
                continue

            visited.add(current_cell)
            self.path.append((current_cell, False))

            if current_cell == goal:
                self.solution_cells = path
                for cell, sol in self.path:
                    if cell in self.solution_cells:
                        self.path.append((cell, True))
                    else:
                        self.path.append((cell, False))
                return dir

            for nx, ny, d in self.reachable_neighbors(current_cell):
                n = (nx, ny)
                if n not in visited:
                    item = (self.priority(n), (n, path + [n], dir + [d]))
                    heapq.heappush(fringe, item)
        return []
