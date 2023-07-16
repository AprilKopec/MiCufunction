from utils import Time

def rest(string):
    return string.split(" ", 1)[1]

class Say:
    takes_block = False
    def __init__(self, stack: list, line: str, args: list[str]) -> None:
      self.parent = stack[-1]
      self.text = [f'{self.parent.prefix()} tellraw @a "{rest(line)}"']

class Command:
    takes_block = False
    def __init__(self, stack: list, line: str, args: list[str]) -> None:
      self.parent = stack[-1]
      self.text = [f"{self.parent.prefix()} {rest(line)}"]

class Wait:
    takes_block = False
    def __init__(self, stack: list, line: str, args: list[str]) -> None:
        self.parent = stack[-1]
        assert hasattr(self.parent, "time"), f"Wait command not supported in {type(self.parent).__name__} blocks."
        self.parent.time += Time(args[1])
        self.text = []

class Comment:
   takes_block = False
   def __init__(self, stack: list, line: str, args: list[str]) -> None:
        self.text = [line.strip()]