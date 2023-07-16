from utils import Time, Objective

class If:
    takes_block = True
    def __init__(self, stack, line, args) -> None:
        self.time = Time(1)
        self.latest_time = Time(1)
        self.objective = Objective(args[1])
        self.text = self.begin()
        self.parent = stack[-1]

        self.timer_number = self.parent.timer_number + 1
        self.timer_name = "t" + self.timer_number

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
          f"execute unless score endCutscene {self.objective.name} matches 1 run schedule function OUTNAME 1t append"
        ]

    def prefix(self) -> str:
        return f"execute if score t {self.objective.name} matches {self.time} run"