from utils import Time
from command_baseclass import MiCufunction_Command
from typing import List

def rest(string):
    return string.split(" ", 1)[1]

class Basic_Command(MiCufunction_Command):
    takes_block = False
    def __init__(self, stack, line: str, args: List[str]):
        self.stack = stack
        self.line = line
        self.args = args

        self.pretext()
        self.text = self.get_text()

    def pretext(self) -> None:
        pass

    def get_text(self) -> List[str]:
        return []

class Say(Basic_Command):
    def get_text(self):
        return [self.prefix(f'tellraw @a "{rest(self.line)}"', self.stack)]

class Command(Basic_Command):
    def get_text(self):
        return [self.prefix(rest(self.line),self.stack)]

class Wait(Basic_Command):
    def pretext(self):
        self.parent = self.find_time_owner(self.stack)
        self.parent.time += Time(self.args[1])

class Comment(Basic_Command):
    def get_text(self):
        return [self.line.strip()]