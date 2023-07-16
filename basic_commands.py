from cutscene import Cutscene
from utils import Time

class Say:
    takes_block = False
    def __init__(self, stack: list, line: str, args: list[str]) -> None:
      self.text = f'tellraw @a "{line[4:]}"'

class Command:
    takes_block = False
    def __init__(self, stack: list, line: str, args: list[str]) -> None:
      self.text = line[8:]

class Wait:
    takes_block = False
    def __init__(self, stack: list, line: str, args: list[str]) -> None:
        cutscene = stack[-1]
        assert(isinstance(cutscene, Cutscene))
        cutscene.time += Time(args[1])
        self.text = None

class Comment:
   takes_block = False
   def __init__(self, stack: list, line: str, args: list[str]) -> None:
      self.text = line.strip()