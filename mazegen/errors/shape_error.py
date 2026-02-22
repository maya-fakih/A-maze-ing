from .base_error import MazeError


class ShapeError(MazeError):
    """Exception raised for shape-related errors"""

    def __init__(
        self,
        message: str,
        shape_name: str | None = None,
        error_code: str = "SHAPE_ERR",
    ) -> None:
        """Initialize a ShapeError instance."""
        self.shape_name = shape_name
        super().__init__(message, error_code)

    def __str__(self) -> str:
        """Return a string representation of the instance."""
        base = super().__str__()
        if self.shape_name:
            return f"{base} - Shape: {self.shape_name}"
        return base
