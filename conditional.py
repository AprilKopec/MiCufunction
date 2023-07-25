from utils import Time
from copy import copy
from command_baseclass import Control_Flow

class If(Control_Flow):
    takes_block = True
    def __init__(self, stack, line, args) -> None:
        self.parent = stack[-1]
        self.condition = " ".join(args[1:-1])
        self.condition_name = self.add_number("condition", self.depth)
        self.condition_value = "1" # We will change this to 0 for else
        super().__init__(stack, line, args)

    def begin(self) -> list[str]:
        # This is a little hacky but it makes the camera slightly less incompatible with conditionals
        self.camera = copy(self.parent.camera)
        text = [
          f"{self.condition} run scoreboard players set {self.condition_name} {self.condition_value}"
          f"execute if score {self.condition_name} matches {self.condition_value} run scoreboard players set {self.parent.pause_name} {self.parent.objective.name} 1",
          f"execute if score {self.condition_name} matches {self.condition_value} unless score {self.pause_name} {self.objective.name} matches 1 run scoreboard players add {self.timer_name} {self.objective.name} 1",
          f"execute if score {self.condition_name} matches {self.condition_value} run scoreboard players set {self.end_name} {self.objective.name} 0"
        ]
        return ["    " + self.add_prefix(line) for line in text] + [""]

    def end(self, else_block: bool = False):
        if not else_block:
            self.parent.time += Time(1) # We want the cutscene to wait until the tick after the if block executes
        self.latest_time = max(self.latest_time, self.time)
        text = [
          f'execute if score {self.condition_name} matches {self.condition_value} if score {self.timer_name} {self.objective.name} matches {self.latest_time} run scoreboard players set {self.end_name} {self.objective.name} 1',
          f'execute if score {self.condition_name} matches {self.condition_value} if score {self.end_name} {self.objective.name} matches 1 run scoreboard players set {self.timer_name} {self.objective.name} 0',
          f'execute if score {self.condition_name} matches {self.condition_value} if score {self.end_name} {self.objective.name} matches 1 run scoreboard players set {self.parent.pause_name} {self.parent.objective.name} 0'
        ]
        return [""] + ["    " + self.add_prefix(line) for line in text]

    def give_prefix(self) -> str:
        return "    " + self.add_prefix(f"execute if score {self.condition_name} matches {self.condition_value} if score {self.timer_name} {self.objective.name} matches {self.time} run")
    
class Else(If):
    pass