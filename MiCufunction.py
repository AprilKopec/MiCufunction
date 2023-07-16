import sys
from cutscene import Cutscene
from duration import Duration
from utils import Time
from basic_commands import Say, Command, Wait, Comment

OUTNAME = sys.argv[2]

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
            if line == "" or line.startswith("#"):
                command_type = Comment
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


def main():
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

main()