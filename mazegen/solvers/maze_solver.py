from abc import ABC, abstractmethod
from ..generators.maze_generator import MazeGenerator


class MazeSolver(ABC):
    """Abstract base class for maze solvers"""
    
    def __init__(self, maze: MazeGenerator) -> None:
        self.maze = maze
        self.solution_cells = []

    def reachable_neighbors(self, cell: tuple) -> list:
        """Returns a list from the neighbors of a cell"""
        nx, ny = cell
        reachable = []
        for nx, ny, direction in self.maze.get_neighbors(cell):
            if not self.maze.has_wall(cell, direction):
                reachable.append((nx, ny, direction))
        return reachable

    @abstractmethod
    def solve(self) -> list:
        """Abstract method to solve the maze and return the solution path"""
        pass
