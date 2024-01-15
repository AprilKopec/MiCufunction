import sys
from function import Function
from duration import Duration
from conditional import If
from camera import Camera
from close_block import Close_Block
from basic_commands import Say, Command, Wait, Comment
from utils import get_filename

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

    def __init__(self, default_file) -> None:
        self.stack = []
        self.outlines = {}
        self.current_file = [default_file]

        implicit_func_line = "function " + default_file + " {"
        self.functions = [Function(self.stack, implicit_func_line, implicit_func_line.split(" "))]

    def add_command(self, line: str, line_num: int):
        line = line.strip()
        args = line.split(' ')

        command_type = get_command_type(line, args, line_num)

        try:
            item = command_type(self.stack, line, args)

            if command_type.has_filename:
                self.current_file.append(item.filename) # type: ignore
                self.outlines[self.current_file[-1]] = []

            if len(self.current_file) != 0 or command_type != Comment:
              self.outlines[self.current_file[-1]] += item.text

            if command_type.can_pop_filename and item.pop_filename: # type: ignore
                self.current_file.pop()
        except Exception as e:
            print(f"Error on line {line_num}: {e.args[0]}")
            raise

        if command_type.takes_block:
            assert args[-1] == "{", f"Error on line {line_num}: Missing {{"
            self.stack.append(item)

    def end_program(self):
        assert len(self.stack) == 1, "The length of the function stack should be 1 when the line ends"
        self.add_command("}", -1)


def get_default_file(filename):
    split = filename.split("/")
    namespace_index = -1
    for i in range(len(split)):
        if split[i] == "functions":
            namespace_index = i - 1
            break
    assert namespace_index >= 0, "No file name provided, and unable to make a default name by looking at .micufunction file's location in datapack"
    unsplit = filename[namespace_index] + ":" + filename[namespace_index+1:].join("/")
    return unsplit



def main():
    FILENAME = sys.argv[1]
    if(FILENAME.split('.')[-1].lower() != "micufunction"):
        raise Exception(".micufunction file not provided")
    import pathlib

    with open(FILENAME, 'r', encoding='utf-8') as infile:
        lines = infile.readlines()
        program = Program(get_default_file(FILENAME))
        for i in range(len(lines)):
            program.add_command(lines[i], i+1)
        for filename, lines in program.outlines.items():
            root = pathlib.Path(sys.argv[2])
            path = root.joinpath(filename)
            assert path.relative_to(root) # path traversal
            path.parent.mkdir(parents=True,exist_ok=True)
            with path.open('w') as file:
                file.writelines(line + "\n" for line in lines)


main()