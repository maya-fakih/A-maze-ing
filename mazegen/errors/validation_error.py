from .generation_error import GenerationError


class ValidationError(GenerationError):
    """Exception raised when maze validation fails"""

    def __init__(
        self,
        message: str,
        invalid_cells: list[tuple[int, int]] | None = None,
        error_code: str = "VAL_ERR",
    ) -> None:
        """
            Initialize validation-stage error. Args: message error text,
            invalid_cells optional invalid coordinates, error_code code tag.
            Returns: None.
        """
        self.invalid_cells = invalid_cells or []
        super().__init__(message, error_code, stage="validation")

    def __str__(self) -> str:
        """
            Format validation error details. Args: self error instance.
            Returns: Formatted error string.
        """
        base = super().__str__()
        if self.invalid_cells and len(self.invalid_cells) <= 10:
            cells_str = ", ".join(str(cell) for cell in self.invalid_cells)
            return f"{base}\n  Invalid cells: {cells_str}"
        elif self.invalid_cells:
            return f"{base}\n  {len(self.invalid_cells)} invalid cells found"
        return base
