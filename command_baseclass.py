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

    # This is a step towards having top level commands other than function        
    def find_prefix(self, stack):
        for item in stack[::-1]:
            if hasattr(item, 'prefix'):
                return item.prefix()
            return None
            
    def add_prefix(self, text: str, stack) -> str:
        text_prefix = self.find_prefix(stack)
        return " ".join([string for string in [text_prefix, text] if string is not None])
        

class Control_Flow(MiCufunction_Command):
    takes_block = True

    def __init__(self, stack: List[MiCufunction_Command], line: str, args: List[str]):
        self.stack = stack
        self.line = line
        self.args = args

        # Eventually we can do the "don't bother with timing if there's no wait or duration" optimization
        self.time = Time(1)
        self.latest_time = Time(1)

        self.objective = self.get_objective()
        self.depth = self.get_depth()
        self.timer_name = self.add_number("t", self.depth)
        self.pause_name = self.add_number("pause", self.depth)
        self.end_name = self.add_number("end", self.depth)

        self.text = self.begin()

    def get_objective(self) -> Objective:
        for item in self.stack[::-1]:
            if hasattr(item, 'objective'):
                return item.objective
            
    def get_depth(self) -> int:
        for item in self.stack[::-1]:
            if hasattr(item, 'depth'):
                return item.depth + 1
        return 0
    
    def add_number(self, name: str, n: int) -> str:
        return name if n == 0 else name + str(n)
            
    @abstractmethod
    def begin(self) -> list[str]:
        pass

    @abstractmethod
    def end(self) -> list[str]:
        pass