from cutscene import Cutscene
from utils import Time

def rest(string):
    return string.split(" ", 1)[1]

class Close_Block:
    takes_block = True
    parent = None
    can_wait = True
    def __init__(self, stack, line, args) -> None:
        self.item = stack.pop()
        self.text = self.item.end()
    
    def prefix(self):
        return self.item.prefix()

class Say:
    takes_block = False
    def __init__(self, stack: list, line: str, args: list[str]) -> None:
      self.text = [f'tellraw @a "{rest(line)}"']

class Command:
    takes_block = False
    def __init__(self, stack: list, line: str, args: list[str]) -> None:
      self.text = [rest(line)]

class Wait:
    takes_block = False
    def __init__(self, stack: list, line: str, args: list[str]) -> None:
        cutscene = stack[-1]
        assert(isinstance(cutscene, Cutscene))
        cutscene.time += Time(args[1])
        self.text = []

class Comment:
   takes_block = False
   def __init__(self, stack: list, line: str, args: list[str]) -> None:
        self.text = [line.strip()]