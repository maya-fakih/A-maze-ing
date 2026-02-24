from .base_error import MazeError


class SolverError(MazeError):
    """Exception raised during maze solving process"""

    def __init__(
        self,
        message: str,
        error_code: str = "SOLVE_ERR",
        algorithm: str | None = None,
    ) -> None:
        """
            Initialize solver-stage error. Args: message error text, error_code
            code tag, algorithm optional solver name. Returns: None.
        """
        self.algorithm = algorithm
        super().__init__(message, error_code)

    def __str__(self) -> str:
        """
            Format solver error details. Args: self error instance. Returns:
            Formatted error string.
        """
        base = super().__str__()
        if self.algorithm:
            return f"{base} - Algorithm: {self.algorithm}"
        return base
