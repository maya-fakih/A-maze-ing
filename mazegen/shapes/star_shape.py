from .shape_generator import Shape
import math


class Star(Shape):
    def __init__(self, width: int, height: int, points: int = 5) -> None:
        """Initialize a Star instance."""
        super().__init__(width, height)
        self.points = points

    def generate(self) -> list:
        """Generate the value."""
        coords = set()
        vertices = []

        outer_r = self.r
        inner_r = self.r * 0.5
        total_vertices = self.points * 2

        for i in range(total_vertices):
            angle = math.pi * i / self.points
            r = outer_r if i % 2 == 0 else inner_r

            x = int(round(self.center_x + r * math.cos(angle)))
            y = int(round(self.center_y + r * math.sin(angle)))

            vertices.append((x, y))

        def draw_line(x1: int, y1: int, x2: int, y2: int) -> None:
            """Draw line."""
            dx = abs(x2 - x1)
            dy = abs(y2 - y1)
            sx = 1 if x1 < x2 else -1
            sy = 1 if y1 < y2 else -1
            err = dx - dy

            while True:
                coords.add((x1, y1))
                if x1 == x2 and y1 == y2:
                    break
                e2 = 2 * err
                if e2 > -dy:
                    err -= dy
                    x1 += sx
                if e2 < dx:
                    err += dx
                    y1 += sy

        for i in range(len(vertices)):
            x1, y1 = vertices[i]
            x2, y2 = vertices[(i + 1) % len(vertices)]
            draw_line(x1, y1, x2, y2)

        return list(coords)
