from .base_error import MazeError


class GenerationError(MazeError):
    """Exception raised during maze generation process"""

    def __init__(
        self,
        message: str,
        error_code: str = "GEN_ERR",
        stage: str | None = None,
    ) -> None:
        """Initialize a GenerationError instance."""
        self.stage = stage
        super().__init__(message, error_code)

    def __str__(self) -> str:
        """Return a string representation of the instance."""
        base = super().__str__()
        if self.stage:
            return f"{base} - Failed during: {self.stage}"
        return base
