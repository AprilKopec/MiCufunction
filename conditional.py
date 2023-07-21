from utils import Time
from copy import copy
from command_baseclass import Control_Flow

class If(Control_Flow):
    takes_block = True
    def __init__(self, stack, line, args) -> None:
        self.parent = stack[-1]
        self.condition = "execute if " + " ".join(args[1:-1])
        super().__init__(stack, line, args)
        

    def begin(self) -> list[str]:
        # This is a little hacky but it makes the camera slightly less incompatible with conditionals
        self.camera = copy(self.parent.camera)
        text = [
          f"{self.condition} run scoreboard players set {self.parent.pause_name} {self.parent.objective.name} 1",
          f"{self.condition} unless score {self.pause_name} {self.objective.name} matches 1 run scoreboard players add {self.timer_name} {self.objective.name} 1",
          f"{self.condition} run scoreboard players set {self.end_name} {self.objective.name} 0"
        ]
        return ["    " + self.add_prefix(line) for line in text] + [""]

    def end(self):
        self.parent.time += Time(1) # We want the cutscene to wait until the tick after the if block executes
        self.latest_time = max(self.latest_time, self.time)
        text = [
          f'{self.condition} if score {self.timer_name} {self.objective.name} matches {self.latest_time} run scoreboard players set {self.end_name} {self.objective.name} 1',
          f'{self.condition} if score {self.end_name} {self.objective.name} matches 1 run scoreboard players set {self.timer_name} {self.objective.name} 0',
          f'{self.condition} if score {self.end_name} {self.objective.name} matches 1 run scoreboard players set {self.parent.pause_name} {self.parent.objective.name} 0'
        ]
        return [""] + ["    " + self.add_prefix(line) for line in text]

    def give_prefix(self) -> str:
        return "    " + self.add_prefix(f"{self.condition} if score {self.timer_name} {self.objective.name} matches {self.time} run")