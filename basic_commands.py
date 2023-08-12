from utils import Time
from command_baseclass import MiCufunction_Command
from typing import List

def rest(string):
    return string.split(" ", 1)[1]

class Basic_Command(MiCufunction_Command):
    def __init__(self, stack, line: str, args: List[str]):
        super().__init__(stack, line, args)

        self.pretext()
        self.text = self.get_text()

    def pretext(self) -> None:
        pass

    def get_text(self) -> List[str]:
        return []


class Say(Basic_Command):
    def get_text(self):
        return [self.add_prefix(f'tellraw @a "{rest(self.line)}"')]

class Command(Basic_Command):
    def get_text(self):
        return [self.add_prefix(rest(self.line))]

class Wait(Basic_Command):
    def pretext(self):
        self.timekeeper = self.find_timekeeper(self.stack)
        self.timekeeper.time += Time(self.args[1])

class Comment(Basic_Command):
    def get_text(self):
        return [self.line.strip()]