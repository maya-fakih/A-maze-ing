from .base_error import MazeError


class GenerationError(MazeError):
    """Exception raised during maze generation process"""

    def __init__(
        self,
        message: str,
        error_code: str = "GEN_ERR",
        stage: str | None = None,
    ) -> None:
        """
            Initialize generation-stage error. Args: message error text,
            error_code code tag, stage optional stage name. Returns: None.
        """
        self.stage = stage
        super().__init__(message, error_code)

    def __str__(self) -> str:
        """
            Format generation error details. Args: self error instance.
            Returns: Formatted error string.
        """
        base = super().__str__()
        if self.stage:
            return f"{base} - Failed during: {self.stage}"
        return base
