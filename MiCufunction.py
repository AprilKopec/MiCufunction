import sys
from cutscene import Cutscene
from duration import Duration
from basic_commands import Say, Command, Wait, Comment, Close_Block

supported_commands = {"cutscene": Cutscene,
                      "duration": Duration,
                      "say": Say,
                      "command": Command,
                      "wait": Wait,
                      "}": Close_Block}

def get_command_type(line, args):
    if line == "" or line.startswith("#"):
        command_type = Comment
    else:
        command_type = supported_commands[args[0]]
    return command_type

class Program:
    def __init__(self) -> None:
        self.stack = []
        self.outlines = []

    def add_command(self, line: str, line_num: int):
        line = line.strip()
        args = line.split(' ')
        command_type = get_command_type(line, args)

        try:
            item = command_type(self.stack, line, args)
            self.outlines += item.text
        except AssertionError as e:
            raise AssertionError(f"Error on line {line_num}: {e.args[0]}")

        if command_type.takes_block:
            assert args[-1] == "{", f"Error on line {line_num}: Missing {{"
            self.stack.append(item)

    def walkStack(self, typ: type):
        for item in reversed(self.stack):
            if isinstance(item, typ):
                return item


def main():
    # FILENAME = sys.argv[1]
    FILENAME = "example.micufunction"
    if(FILENAME.split('.')[-1].lower() != "micufunction"):
        raise Exception(".micufunction file not provided")

    with open(FILENAME, 'r') as infile:
        lines = infile.readlines()
        program = Program()
        for i in range(len(lines)):
            program.add_command(lines[i], i)
        for line in program.outlines:
            print(line)

main()