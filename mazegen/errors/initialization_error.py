from .generation_error import GenerationError


class InitializationError(GenerationError):
    """Maze initialization fails due to invalid parameters"""

    def __init__(self, message, invalid_params=None, error_code="INIT_ERR"):
        self.invalid_params = invalid_params or {}
        super().__init__(message, error_code, stage="initialization")

    def __str__(self):
        base = super().__str__()
        if self.invalid_params:
            params_str = ", ".join(
                f"{k}: {v}" for k, v in self.invalid_params.items())
            return f"{base}\n  Invalid parameters: {params_str}"
        return base
