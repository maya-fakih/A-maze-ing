class MazeError(Exception):
    """Base exception for all maze-related errors"""

    def __init__(self, message: str, error_code: str | None = None) -> None:
        """Initialize a MazeError instance."""
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)

    def __str__(self) -> str:
        """Return a string representation of the instance."""
        if self.error_code:
            return f"[{self.error_code}] {self.message}"
        return self.message
