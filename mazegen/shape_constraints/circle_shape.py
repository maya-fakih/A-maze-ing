from .shape_generator import Shape

class Circle(Shape):
    def generate(self) -> list:
        coords = []
        for y in range(self.height):
            for x in range(self.width):
                dx = x - self.center_x
                dy = y - self.center_y
                distance = (dx**2 + dy**2)**0.5
                if abs(distance - self.r) < 0.5:
                    coords.append((x, y))
        return coords