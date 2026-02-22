from .generation_error import GenerationError


class InitializationError(GenerationError):
    """Maze initialization fails due to invalid parameters"""

    def __init__(
        self,
        message: str,
        invalid_params: dict | None = None,
        error_code: str = "INIT_ERR",
    ) -> None:
        """Initialize a InitializationError instance."""
        self.invalid_params = invalid_params or {}
        super().__init__(message, error_code, stage="initialization")

    def __str__(self) -> str:
        """Return a string representation of the instance."""
        base = super().__str__()
        if self.invalid_params:
            params_str = ", ".join(
                f"{k}: {v}" for k, v in self.invalid_params.items())
            return f"{base}\n  Invalid entry and exit: {params_str}"
        return base
