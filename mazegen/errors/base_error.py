class MazeError(Exception):
    """Base exception for all maze-related errors"""

    def __init__(self, message: str, error_code: str | None = None) -> None:
        """Initialize base maze exception. Args: message human-readable error text, error_code optional code tag. Returns: None."""
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)

    def __str__(self) -> str:
        """Format exception for display. Args: self error instance. Returns: Formatted error string."""
        if self.error_code:
            return f"[{self.error_code}] {self.message}"
        return self.message
