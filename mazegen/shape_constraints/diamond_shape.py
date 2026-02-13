import math
from shape_generator import Shape

class Diamond(Shape):
    def generate(self) -> list:
        coords = []
        for y in range(self.height):
            for x in range (self.width):
                if (abs(abs(x - self.center_x) + abs(y - self.center_y) - self.r) < 0.5):
                    coords.append((x, y))
        return (coords)