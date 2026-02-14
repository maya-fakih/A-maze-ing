from .base_error import MazeError

class SolverError(MazeError):
    """Exception raised during maze solving process"""
    
    def __init__(self, message, error_code="SOLVE_ERR", algorithm=None):
        self.algorithm = algorithm
        super().__init__(message, error_code)
    
    def __str__(self):
        base = super().__str__()
        if self.algorithm:
            return f"{base} - Algorithm: {self.algorithm}"
        return base