import sys
import re
from functools import total_ordering
from typing import Union

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


class Cutscene:
    takes_block = True
    parent = None
    can_wait = True
    def __init__(self, stack, args) -> None:
        self.time = Time(1)
        self.latest_time = Time(1)
        self.objective = Objective(args[1])
        pass

    def begin(self) -> list[str]:
        return [
          "### Cutscene setup ###",
          f"scoreboard objectives add {self.objective.name} dummy",
          f"scoreboard players add t {self.objective.name} 1",
          f"scoreboard players set endCutscene {self.objective.name} 0",
          "",
          "### Cutscene ###"
        ]

    def end(self):

        self.latest_time = max(self.latest_time, self.time)
        return [
          "",
          "### Cutscene Cleanup ###",
          f'execute if score t {self.objective.name} matches {self.latest_time} run scoreboard players set endCutscene {self.objective.name} 1',
          f'execute if score endCutscene {self.objective.name} matches 1 run scoreboard players set t {self.objective.name} 0',
          "",
          "### Run cutscene every tick ###",
          f"execute unless score endCutscene {self.objective.name} matches 1 run schedule function {OUTNAME} 1t append"
        ]

    def prefix(self) -> str:
        return f"execute if score t {self.objective.name} matches {self.time} run"

class Duration:
    takes_block = True
    def __init__(self, stack, args) -> None:
        self.parent = stack[-1]
        self.duration = Time(args[1])

    def begin(self) -> list[str]:
        return []

    def prefix(self) -> str:
        return f'execute if score t {self.parent.objective.name} matches {self.parent.time.ticks}..{self.parent.time+self.duration} run tellraw @a "{line[4:]}"'

    def end(self)-> list[str]:
        return []

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