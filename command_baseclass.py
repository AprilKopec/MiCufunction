from utils import Objective, Time
from abc import ABC, abstractmethod
from typing import List

class MiCufunction_Command(ABC):
    @abstractmethod
    def __init__(self, stack, line: str, args: List[str]):
        pass

    def find_time_owner(self, stack):
        for item in stack[::-1]:
            if hasattr(item, 'time'):
                return item
            
    def find_prefix(self, stack) -> str:
        for item in stack[::-1]:
            if hasattr(item, 'prefix'):
                return item.prefix()
            
    def add_prefix(self, text: str, stack) -> str:
        text_prefix = self.find_prefix(stack)
        return " ".join([text_prefix, text])

class Control_Flow_Command(MiCufunction_Command):
    takes_block = True

    def find_objective(self, stack) -> Objective:
        for item in stack[::-1]:
            if hasattr(item, 'objective'):
                return item.objective
            
    @abstractmethod
    def begin(self) -> list[str]:
        pass

    @abstractmethod
    def end(self) -> list[str]:
        pass