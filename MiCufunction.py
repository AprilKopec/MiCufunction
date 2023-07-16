import sys
import re
from functools import total_ordering
from typing import Union

from cutscene import Cutscene
from duration import Duration

OUTNAME = sys.argv[2]

class Objective:
    def __init__(self, name: str) -> None:
        if re.match(r'^[a-zA-Z0-9_.+-]+$',name) is None:
           raise ValueError(name + "is not a valid objective name")
        self.name = name

# Takes a string which contains either an integer, or an number followed by s or t
# If it's a plain integer or is followed by t, it is interpreted as a number of ticks
# If it's followed by s it is interpreted as a number of seconds
@total_ordering
class Time:
    def __init__(self, time: Union[str, int]) -> None:
        if isinstance(time, str):
            if time[-1] == "s":
                ticks = int(20*float(time[0:-1]))
            elif time[-1] == "t":
                ticks = int(time[0:-1])
            else:
                ticks = int(time)
        else:
            ticks = time
        self.ticks = ticks

    def __add__(self, other):
        return Time(self.ticks + other.ticks)
    def __lt__(self, other):
        return self.ticks < other.ticks
    def __eq__(self, other):
        return self.ticks == other.ticks
    def __str__(self) -> str:
        return str(self.ticks)

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