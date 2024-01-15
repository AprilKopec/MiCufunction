from utils import Objective, Camera_Position, get_filename
from command_baseclass import Control_Flow

class Function(Control_Flow):
    takes_block = True
    has_filename = True
    def __init__(self, stack, line, args) -> None:
        self.filename = get_filename(args[1])
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
          # Make sure the scoreboard objective exists
          f"scoreboard objectives add {self.objective} dummy",
          # Increment timer unless part of the function has made a separate timer
          f"execute unless score {self.pause_name} {self.objective} matches 1 run scoreboard players add {self.timer_name} {self.objective} 1",
          # Make sure function doesn't end early and can replay
          f"scoreboard players set {self.end_name} {self.objective} 0",
          "",
          "### Cutscene ###"
        ]

    def end(self):
        self.latest_time = max(self.latest_time, self.time)
        return [
          "",
          "### Cutscene Cleanup ###",
          # End the function after the last event ends
          f'execute if score {self.timer_name} {self.objective} matches {self.latest_time} run scoreboard players set {self.end_name} {self.objective} 1',
          # Reset the timer for next time function is used
          f'execute if score {self.end_name} {self.objective} matches 1 run scoreboard players set {self.timer_name} {self.objective} 0',
          "",
          "### Run cutscene every tick ###",
          # Check that global timer has incremented since the last time the function was ran; force-quit the cutscene if it's run multiple times in the same tick
          f"execute store result score temp {self.objective} run time query gametime",
          f"scoreboard players operation global_timer {self.objective} -= temp {self.objective}",
          f"execute if score global_timer {self.objective} matches 0 run scoreboard players set {self.forcequit} {self.objective} 1",
          f"scoreboard players operation global_timer {self.objective} = temp {self.objective}",
          # Schedule function if not over and not forcequit
          f"execute unless score {self.end_name} {self.objective} matches 1 unless score {self.forcequit} {self.objective} matches 1 run schedule function {self.function_name} 1t replace"
          # Maybe we want to set this up so that if the cutscene runs multiple times it only resets the extras? Might be more resilient to glitches then
        ]

    def give_prefix(self) -> str:
        return f"execute if score {self.timer_name} {self.objective} matches {self.time} run"