from .base_error import MazeError


class ShapeError(MazeError):
    """Exception raised for shape-related errors"""

    def __init__(self, message, shape_name=None, error_code="SHAPE_ERR"):
        self.shape_name = shape_name
        super().__init__(message, error_code)

    def __str__(self):
        base = super().__str__()
        if self.shape_name:
            return f"{base} - Shape: {self.shape_name}"
        return base
