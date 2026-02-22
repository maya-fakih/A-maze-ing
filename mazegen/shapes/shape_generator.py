from abc import ABC, abstractmethod


class Shape(ABC):
    def __init__(self, width: int, height: int) -> None:
        """Initialize a Shape instance."""
        self.width = width
        self.height = height
        self.center_x = (width - 1) // 2
        self.center_y = (height - 1) // 2
        self.r = (min(width, height) - 1) / 2

    @abstractmethod
    def generate(self) -> list:
        """Generate the value."""
        pass
