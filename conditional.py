from utils import Time
from copy import copy
from command_baseclass import Control_Flow

class If(Control_Flow):
    takes_block = True
    def __init__(self, stack, line, args) -> None:
        # This deserves refactoring
        self.parent = stack[-1]
        self.condition = " ".join(args[1:-1])
        self.condition_value = "1" # We will change this to 0 for else
        self.stack = stack
        self.condition_name = self.add_number("condition", self.get_depth())
        self.condition_checked = self.add_number("condition_checked", self.get_depth())
        super().__init__(stack, line, args)    
    
    def begin(self) -> list[str]:
        # You have to write this string a lot
        self.execute_if_condition = f'execute if score {self.condition_name} {self.objective} matches {self.condition_value}'

        # This is a little hacky but it makes camera slide slightly less incompatible with conditionals
        self.camera = copy(self.parent.camera)

        # Refactor this later; the condition_checked value is unnecessary now that we increment the parent timer after setting up the if block
        text0 = [
          # Check condition, store result
          f"execute if {self.condition} unless score {self.condition_checked} {self.objective} matches 1 run scoreboard players set {self.condition_name} {self.objective} 1",
          f"execute unless score {self.condition_name} {self.objective} matches 1 unless score {self.condition_checked} {self.objective} matches 1 run scoreboard players set {self.condition_name} {self.objective} 0",
          # We only want to check condition once
          f"scoreboard players set {self.condition_checked} {self.objective} 1",
          # Make sure function can replay correctly
          f"{self.execute_if_condition} run scoreboard players set {self.end_name} {self.objective} 0",
          # Increment parent timer by one so that if an If Block starts the same tick that another command was executed, that command isn't executed the entire time the parent timer is paused
          f"scoreboard players add {self.parent.timer_name} {self.objective} 1"     
        ]
        text0 = ["    " + self.add_prefix(line) for line in text0]
        self.parent.time += Time(1)
        text1 = [
          # If condition met, pause parent timer
          f"{self.execute_if_condition} run scoreboard players set {self.parent.pause_name} {self.objective} 1",
          # If condition met and not paused by a further if block, increment timer
          f"{self.execute_if_condition} unless score {self.pause_name} {self.objective} matches 1 run scoreboard players add {self.timer_name} {self.objective} 1"
        ]
        text1 = ["    " + self.add_prefix(line) for line in text1]
        return text0 + text1 + ["\n"]

    def end(self, else_block: bool = False):
        self.latest_time = max(self.latest_time, self.time)
        text = [
          # End the block after the last event ends
          f'{self.execute_if_condition} if score {self.timer_name} {self.objective} matches {self.latest_time} run scoreboard players set {self.end_name} {self.objective} 1',
          # Reset the timer for next time function is used
          f'{self.execute_if_condition} if score {self.end_name} {self.objective} matches 1 run scoreboard players set {self.timer_name} {self.objective} 0',
          # Reset condition_checked
          f'{self.execute_if_condition} if score {self.end_name} {self.objective} matches 1 run scoreboard players set {self.parent.pause_name} {self.parent.objective.name} 0'
        ]
        output = ["\n"] + ["    " + self.add_prefix(line) for line in text]

        if not else_block:
            output += [self.add_prefix(f"execute if score {self.end_name} {self.objective} matches 1 run scoreboard players add {self.parent.timer_name} {self.objective} 1")]
            self.parent.time += Time(1)
        return output

    def give_prefix(self) -> str:
        return "    " + self.add_prefix(f"{self.execute_if_condition} if score {self.timer_name} {self.objective} matches {self.time} run")
    
# Probably if and else should both descend from a superclass but whatever
class Else(If):
    takes_block = True
    def __init__(self, if_block) -> None:
        # This should probably be refactored so that it can call If's __init__ or something
        assert isinstance(if_block, If), "else must follow if"
        self.parent = if_block.parent
        self.condition = if_block.condition # Unused, but crashes when you call super().begin() if not set. Maybe refactor?
        self.condition_name = if_block.condition_name
        self.condition_value = "0"
        self.condition_checked = if_block.condition_checked
        self.execute_if_condition = f'execute if score {self.condition_name} {if_block.objective} matches {self.condition_value}'
        Control_Flow.__init__(self, if_block.stack, if_block.line, if_block.args)

    def begin(self) -> list[str]:
        # This is a copy paste of part of If so it should probably be refactored
        text = [
          # If condition met, pause parent timer
          f"{self.execute_if_condition} run scoreboard players set {self.parent.pause_name} {self.objective} 1",
          # If condition met and not paused by a further if block, increment timer
          f"{self.execute_if_condition} unless score {self.pause_name} {self.objective} matches 1 run scoreboard players add {self.timer_name} {self.objective} 1",
          # Make sure function can replay correctly
          f"{self.execute_if_condition} run scoreboard players set {self.end_name} {self.objective} 0"
        ]
        return ["    " + self.add_prefix(line) for line in text]