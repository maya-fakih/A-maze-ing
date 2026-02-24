from abc import ABC, abstractmethod


class Shape(ABC):
    def __init__(self, width: int, height: int) -> None:
        """Store shape canvas dimensions and center. Args: width canvas width, height canvas height. Returns: None."""
        self.width = width
        self.height = height
        self.center_x = (width - 1) // 2
        self.center_y = (height - 1) // 2
        self.r = (min(width, height) - 1) / 2

    @abstractmethod
    def generate(self) -> list:
        """Generate coordinates outlining the shape. Args: self shape instance. Returns: List of border coordinates."""
        pass
