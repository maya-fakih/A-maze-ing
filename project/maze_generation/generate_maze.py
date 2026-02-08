from abc import ABC, abstractmethod
from typing import Any


class MazeGenerator(ABC):
    @abstractmethod
    def __init__(self, width, hight) -> None:
        pass
    
    @abstractmethod
    def generator(self) -> Any:
        pass

