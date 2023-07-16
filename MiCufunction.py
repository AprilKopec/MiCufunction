import sys
from cutscene import Cutscene
from duration import Duration
from utils import Objective, Time

OUTNAME = sys.argv[2]

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

supported_commands = {"cutscene": Cutscene,
                      "duration": Duration,
                      "say": Say,
                      "command": Command,
                      "wait": Wait}

class Program:
    def __init__(self) -> None:
        self.stack = []
        self.outlines = []

    def add_command(self, line: str):
        line = line.strip()

        if line == "" or line.startswith("#"):
            return

        args = line.split(' ')
        if line == "}":
            item = self.stack.pop()
            for text in item.end():
                if text is not None:
                    self.outlines.append(self.stack[-1].prefix() + " " + text if len(self.stack) >= 1 else text)
        else:
            command_type = supported_commands[args[0]]
            if command_type.takes_block:
                assert(args[-1] == "{")
                item = command_type(args)
                for text in item.begin():
                    if text is not None:
                        self.outlines.append(self.stack[-1].prefix() + " " + text if len(self.stack) >= 1 else text)
                self.stack.append(item)
            else:
                text = command_type(self.stack, line, args).text
                if text is not None:
                     self.outlines.append(self.stack[-1].prefix() + " " + text)

    def walkStack(self, typ: type):
        for item in reversed(self.stack):
            if isinstance(item, typ):
                return item


FILENAME = sys.argv[1]
if(FILENAME.split('.')[-1].lower() != "micufunction"):
    raise Exception(".micufunction file not provided")


with open(FILENAME, 'r') as infile:
    lines = infile.readlines()
    program = Program()
    for line in lines:
        program.add_command(line)
    for line in program.outlines:
        print(line)