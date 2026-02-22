from .shape_generator import Shape
import math


class Flower(Shape):
    def __init__(self, width: int, height: int, points: int = 5) -> None:
        """Initialize a Flower instance."""
        super().__init__(width, height)
        self.points = points

    def generate(self) -> list:
        """Generate the value."""
        coords = set()
        steps = max(self.width, self.height) * 8

        for i in range(steps):
            angle = 2 * math.pi * i / steps

            k = self.points
            r_star = self.r * (0.5 + 0.5 * abs(math.cos(k * angle / 2)))

            x = self.center_x + r_star * math.cos(angle)
            y = self.center_y + r_star * math.sin(angle)

            coords.add((round(x), round(y)))

        return list(coords)
