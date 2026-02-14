from .base_error import MazeError

class GenerationError(MazeError):
    """Exception raised during maze generation process"""
    
    def __init__(self, message, error_code="GEN_ERR", stage=None):
        self.stage = stage
        super().__init__(message, error_code)
    
    def __str__(self):
        base = super().__str__()
        if self.stage:
            return f"{base} - Failed during: {self.stage}"
        return base