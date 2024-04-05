from utils import Time
from command_baseclass import MiCufunction_Command
from typing import List
import re

def escape(input):
    return re.sub("[\\\"\']", "\\\\\\g<0>", input)

def rest(string, n: int = 1) -> str:
    return string.split(" ", n)[n]

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
        return [self.add_prefix(f'tellraw @a "{escape(rest(self.line))}"')]

class Command(Basic_Command):
    def get_text(self):
        return [self.add_prefix(rest(self.line))]

class Wait(Basic_Command):
    def pretext(self):
        self.timekeeper = self.find_timekeeper(self.stack)
        if(self.args[1] not in ["until", "while"]):
            try:
                self.timekeeper.time += Time(self.args[1])
            except:
                raise ValueError("Valid arguments for 'wait' are 'until', 'while', or a duration.")

    def get_text(self):
        if(self.args[1] in ["until", "while"]):
            timer_name = self.timekeeper.timer_name
            pause_name = self.timekeeper.pause_name
            objective = self.timekeeper.objective
            b = 1 if self.args[1] == "until" else 0

            text = [self.add_prefix(f'scoreboard players add {timer_name} {objective} 1')]
            self.timekeeper.time += Time(1)

            text1 = [
                f'scoreboard players set {pause_name} {objective} 1',
                f'scoreboard players set temp {objective} 0'
                f'execute if {rest(self.line,2)} run scoreboard players set temp {objective} 1'
                f'execute if score temp {objective} matches {b} run scoreboard players set {pause_name} {objective} 0',
                f'execute if score temp {objective} matches {b} run scoreboard players add {timer_name} {objective} 1'
            ]
            text += [self.add_prefix(line) for line in text1]
            self.timekeeper.time += Time(1)
            return text

        else:
            return []

class Comment(Basic_Command):
    def get_text(self):
        return [self.line.strip()]