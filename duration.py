from utils import Time

class Duration:
    takes_block = True
    def __init__(self, stack, args) -> None:
        self.parent = stack[-1]
        self.duration = Time(args[1])

    def begin(self) -> list[str]:
        return []

    def prefix(self) -> str:
        return f'execute if score t {self.parent.objective.name} matches {self.parent.time.ticks}..{self.parent.time+self.duration} run tellraw @a "{line[4:]}"'

    def end(self)-> list[str]:
        return []