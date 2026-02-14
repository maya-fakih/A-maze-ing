from .shape_generator import Shape


class Heart(Shape):
    def generate(self) -> list:
        coords = []
        scale = min(self.width, self.height) / 30
        
        for y in range(self.height):
            for x in range(self.width):
                nx = (x - self.center_x) / (self.center_x)
                ny = (self.center_y - y) / (self.center_y)
                
                heart_value = (nx**2 + ny**2 - 1)**3 - nx**2 * ny**3
                
                if abs(heart_value) < 0.05:
                    coords.append((x, y))
                    
        return coords