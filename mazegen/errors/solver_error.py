from .base_error import MazeError


class SolverError(MazeError):
    """Exception raised during maze solving process"""

    def __init__(
        self,
        message: str,
        error_code: str = "SOLVE_ERR",
        algorithm: str | None = None,
    ) -> None:
        """Initialize a SolverError instance."""
        self.algorithm = algorithm
        super().__init__(message, error_code)

    def __str__(self) -> str:
        """Return a string representation of the instance."""
        base = super().__str__()
        if self.algorithm:
            return f"{base} - Algorithm: {self.algorithm}"
        return base
