from .maze_solver import MazeSolver
import heapq


class UCSolver(MazeSolver):
    """Uniform Cost Search Agent"""

    def priority(self, path: list) -> int:
        """Priority function for Uniform Cost Search (heuristic only)"""
        return len(path)

    def solve(self) -> list:
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
                    p = dir + [d]
                    item = (self.priority(p), (n, path + [n], p))
                    heapq.heappush(fringe, item)
        return []
