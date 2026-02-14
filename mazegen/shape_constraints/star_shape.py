from .shape_generator import Shape
import math


class Star(Shape):
    def __init__(self, width: int, height: int, points: int = 5):
        super().__init__(width, height)
        self.points = points
        
    def generate(self) -> list:
        coords = []
        
        for y in range(self.height):
            for x in range(self.width):
                dx = x - self.center_x
                dy = y - self.center_y
                
                distance = (dx**2 + dy**2)**0.5
                if distance == 0:
                    continue
                
                angle = math.atan2(dy, dx)
                
                k = self.points
                r_star = self.r * (0.5 + 0.5 * abs(math.cos(k * angle / 2)))
                
                if abs(distance - r_star) < 0.7:
                    coords.append((x, y))
        return coords