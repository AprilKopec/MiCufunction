from utils import Time, Objective

class Cutscene:
    takes_block = True
    def __init__(self, stack, line, args) -> None:
        self.time = Time(1)
        self.latest_time = Time(1)
        self.objective = Objective(args[1])
        
        self.timer_number = 0
        self.timer_name = "t"
        self.pause_name = "pause"
        self.end_name = "endCutscene"

        self.text = self.begin()

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
          f"execute unless score {self.end_name} {self.objective.name} matches 1 run schedule function OUTNAME 1t append"
        ]

    def prefix(self) -> str:
        return f"execute if score {self.timer_name} {self.objective.name} matches {self.time} run"