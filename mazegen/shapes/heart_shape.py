from .shape_generator import Shape
import math


class Heart(Shape):
    def generate(self) -> list:

        coords = set()
        vertices = []

        scale = min(self.width, self.height) / 40

        steps = 1000

        for i in range(steps + 1):
            t = 2 * math.pi * i / steps

            x = 16 * math.sin(t) ** 3
            y = (
                13 * math.cos(t)
                - 5 * math.cos(2 * t)
                - 2 * math.cos(3 * t)
                - math.cos(4 * t)
            )

            px = int(round(self.center_x + x * scale))
            py = int(round(self.center_y - y * scale))

            vertices.append((px, py))

        def draw_line(x1, y1, x2, y2):
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

        for i in range(len(vertices) - 1):
            x1, y1 = vertices[i]
            x2, y2 = vertices[i + 1]
            draw_line(x1, y1, x2, y2)

        return list(coords)
