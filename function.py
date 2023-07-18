from utils import Time, Objective, Camera_Position
from command_baseclass import Control_Flow

class Function(Control_Flow):
    takes_block = True
    def __init__(self, stack, line, args) -> None:
        super.__init__(stack, line, args)

        self.function_name = args[1]

        self.camera = Camera_Position(0, 0, 0)

        self.text = self.begin()

    def get_objective(self) -> Objective:
        return Objective(self.args[1].replace(":",".").replace("/","."))

    def begin(self) -> list[str]:
        return [
          "### Cutscene setup ###",
          f"scoreboard objectives add {self.objective.name} dummy",
          f"execute unless score {self.pause_name} {self.objective.name} matches 1 run scoreboard players add {self.timer_name} {self.objective.name} 1",
          f"scoreboard players set {self.end_name} {self.objective.name} 0",
          "",
          "### Cutscene ###"
        ]

    def end(self):
        self.latest_time = max(self.latest_time, self.time)
        return [
          "",
          "### Cutscene Cleanup ###",
          f'execute if score {self.timer_name} {self.objective.name} matches {self.latest_time} run scoreboard players set {self.end_name} {self.objective.name} 1',
          f'execute if score {self.end_name} {self.objective.name} matches 1 run scoreboard players set {self.timer_name} {self.objective.name} 0',
          "",
          "### Run cutscene every tick ###",
          f"execute unless score {self.end_name} {self.objective.name} matches 1 run schedule function {self.function_name} 1t append"
        ]

    def prefix(self) -> str:
        return f"execute if score {self.timer_name} {self.objective.name} matches {self.time} run"