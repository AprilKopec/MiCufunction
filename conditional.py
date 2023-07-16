from utils import Time

class If:
    takes_block = True
    def __init__(self, stack, line, args) -> None:
        self.parent = stack[-1]
        self.time = Time(1)
        self.latest_time = Time(1)
        self.objective = self.parent.objective
        self.condition = "execute if " + " ".join(args[1:-1])

        self.timer_number = self.parent.timer_number + 1
        self.timer_name = "t" + str(self.timer_number)
        self.pause_name = "pause" + str(self.timer_number)
        self.end_name = "end" + str(self.timer_number)

        self.text = self.begin()

    def begin(self) -> list[str]:
        return [
          f"    {self.parent.prefix()} scoreboard players set {self.parent.pause_name} {self.parent.objective.name} 1",
          f"    {self.parent.prefix()} execute unless score {self.pause_name} {self.objective.name} matches 1 run scoreboard players add {self.timer_name} {self.objective.name} 1",
          f"    {self.parent.prefix()} scoreboard players set {self.end_name} {self.objective.name} 0",
          "",
        ]

    def end(self):
        self.latest_time = max(self.latest_time, self.time)
        return [
          "",
          f'    {self.parent.prefix()} execute if score {self.timer_name} {self.objective.name} matches {self.latest_time} run scoreboard players set {self.end_name} {self.objective.name} 1',
          f'    {self.parent.prefix()} execute if score {self.end_name} {self.objective.name} matches 1 run scoreboard players set {self.timer_name} {self.objective.name} 0',
          f'    {self.parent.prefix()} execute if score {self.end_name} {self.objective.name} matches 1 run scoreboard players set {self.parent.pause_name} {self.parent.objective.name} 0',
          ""
        ]

    def prefix(self) -> str:
        return f"    {self.parent.prefix()} {self.condition} if score {self.timer_name} {self.objective.name} matches {self.time} run"