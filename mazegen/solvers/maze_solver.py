from abc import ABC
from ..generators.maze_generator import MazeGenerator
from typing import List, Tuple


class MazeSolver(ABC):
    """Abstract base class for maze solvers"""

    def __init__(self, maze: MazeGenerator) -> None:
        """
            Initialize solver state for a maze. Args: maze maze generator to
            solve. Returns: None.
        """
        self.maze = maze
        self.solution_cells: List[Tuple[int, int]] = []
        self.animation_path: List[Tuple[Tuple[int, int], bool]] = []

    def reachable_neighbors(self, cell: tuple) -> list:
        """
            Return adjacent cells reachable without crossing walls. Args: cell
            current cell coordinates. Returns: Reachable neighbor tuples.
        """
        nx, ny = cell
        reachable = []
        for nx, ny, direction in self.maze.get_neighbors(cell):
            if not self.maze.has_wall(cell, direction):
                reachable.append((nx, ny, direction))
        return reachable

    def solve(self) -> List[str]:
        """
            Compute move sequence from entry to exit. Args: self solver
            instance. Returns: Direction list representing solution.
        """
        raise NotImplementedError

    def huristic(self, cell: tuple) -> int:
        """
            Estimate Manhattan distance to exit. Args: cell current
            coordinates. Returns: Heuristic distance integer.
        """
        x1, y1 = cell
        x2, y2 = self.maze.exit
        return int(abs(x1 - x2) + abs(y1 - y2))
