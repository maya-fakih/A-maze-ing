from .maze_solver import MazeSolver
from typing import List, Tuple, TypeAlias
import heapq


FringeItem: TypeAlias = Tuple[int, Tuple[Tuple, List, List[str]]]


class AStarSolver(MazeSolver):
    """A* Search Agent"""

    def priority(self, path: list[str], current_cell: tuple[int, int]) -> int:
        """
            Compute A* priority score. Args: path directions taken so far,
            current_cell current cell coordinates. Returns: Priority cost
            integer.
        """
        return len(path) + self.huristic(current_cell)

    def solve(self) -> List[str]:
        """
            Solve maze with A* search. Args: self solver instance. Returns:
            Direction list from entry to exit.
        """
        start = self.maze.entry
        goal = self.maze.exit
        self.animation_path = []
        self.animation_path.append((start, True))

        visited = set()
        fringe: List[FringeItem] = [(0, (start, [start], []))]
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
                    item = (self.priority(p, n), (n, path + [n], p))
                    heapq.heappush(fringe, item)
        return []
