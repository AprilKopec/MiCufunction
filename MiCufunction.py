import sys
from function import Function
from duration import Duration
from conditional import If
from camera import Camera
from close_block import Close_Block
from basic_commands import Say, Command, Wait, Comment

supported_commands = {"function": Function,
                      "duration": Duration,
                      "say": Say,
                      "command": Command,
                      "wait": Wait,
                      "if": If,
                      "camera": Camera, 
                      "}": Close_Block,
                      }

def get_command_type(line, args, line_num):
    if line == "" or line.startswith("#"):
        command_type = Comment
    else:
        assert args[0] in supported_commands, f"Error on line {line_num}: {args[0]} is an invalid command"
        command_type = supported_commands[args[0]]
    return command_type

class Program:
    def __init__(self) -> None:
        self.stack = []
        self.outlines = []

    def add_command(self, line: str, line_num: int):
        line = line.strip()
        args = line.split(' ')

        command_type = get_command_type(line, args, line_num)

        try:
            item = command_type(self.stack, line, args)
            self.outlines += item.text
        except Exception as e:
            print(f"Error on line {line_num}: {e.args[0]}")
            raise

        if command_type.takes_block:
            assert args[-1] == "{", f"Error on line {line_num}: Missing {{"
            self.stack.append(item)

    def walkStack(self, typ: type):
        for item in reversed(self.stack):
            if isinstance(item, typ):
                return item


def main():
    # FILENAME = sys.argv[1]
    FILENAME = "example2.micufunction"
    if(FILENAME.split('.')[-1].lower() != "micufunction"):
        raise Exception(".micufunction file not provided")

    with open(FILENAME, 'r') as infile:
        lines = infile.readlines()
        program = Program()
        for i in range(len(lines)):
            program.add_command(lines[i], i+1)
        for line in program.outlines:
            print(line)

main()