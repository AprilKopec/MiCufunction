from utils import Time, Objective, Camera_Position
from command_baseclass import Control_Flow

class Function(Control_Flow):
    takes_block = True
    def __init__(self, stack, line, args) -> None:
        self.function_name = args[1]
        self.camera = Camera_Position(0, 0, 0)

        # These are only needed for cutscenes, if we implement functions that aren't cutscenes
        self.forcequit = "force_quit"
        self.global_timer = "global_timer"

        super().__init__(stack, line, args)

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
          # Check that the cutscene isn't running multiple times per tick
          f"scoreboard players operation {self.global_timer} {self.objective.name} -= t Tt2GlobalTimer",
          f"execute if score {self.global_timer} {self.objective.name} matches 0 run scoreboard players set {self.forcequit} {self.objective.name} 1",
          f"scoreboard players operation {self.global_timer} {self.objective.name} = t Tt2GlobalTimer",
          # Schedule function if conditions met
          f"execute unless score {self.end_name} {self.objective.name} matches 1 unless score {self.forcequit} {self.objective.name} matches 1 run schedule function {self.function_name} 1t append",
          # If we just leave this set to 1 then it might softlock the player I think
          # Maybe I could copy it to some other scoreboard value first for debug if that seems necessary
          f"scoreboard players set {self.forcequit} {self.objective.name} 0"
        ]

    def give_prefix(self) -> str:
        return f"execute if score {self.timer_name} {self.objective.name} matches {self.time} run"