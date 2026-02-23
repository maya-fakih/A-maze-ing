from abc import ABC
from ..generators.maze_generator import MazeGenerator
from typing import List, Tuple


class MazeSolver(ABC):
    """Abstract base class for maze solvers"""

    def __init__(self, maze: MazeGenerator) -> None:
        """Initialize a MazeSolver instance."""
        self.maze = maze
        self.solution_cells: List[Tuple[int, int]] = []
        self.animation_path: List[Tuple[Tuple[int, int], bool]] = []

    def reachable_neighbors(self, cell: tuple) -> list:
        """Handle reachable neighbors."""
        nx, ny = cell
        reachable = []
        for nx, ny, direction in self.maze.get_neighbors(cell):
            if not self.maze.has_wall(cell, direction):
                reachable.append((nx, ny, direction))
        return reachable

    def solve(self) -> List[str]:
        """Solve the value."""
        raise NotImplementedError

    def huristic(self, cell: tuple) -> int:
        """Handle huristic."""
        x1, y1 = cell
        x2, y2 = self.maze.exit
        return int(abs(x1 - x2) + abs(y1 - y2))
