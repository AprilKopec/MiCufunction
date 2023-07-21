from utils import Time
from command_baseclass import MiCufunction_Command

class Duration(MiCufunction_Command):
    takes_block = True
    def __init__(self, stack, line, args) -> None:
        super().__init__(stack, line, args)
        self.duration = Time(args[1])
        self.timekeeper = self.find_timekeeper(self.stack)
        self.text = self.begin()

    def begin(self) -> list[str]:
        return []

    def give_prefix(self) -> str:
        preprefix = self.get_prefix().split(" ")
        
        # This is almost certainly not the correct way to do this
        assert preprefix[-7] == "if", "Issue with duration's parent"
        assert preprefix[-6] == "score", "Issue with duration's parent"
        assert preprefix[-3] == "matches", "Issue with duration's parent"
        assert preprefix[-2].isdigit() or (preprefix[-2][0] == '-' and preprefix[-2][1:].isdigit()), "Issue with duration's parent"
        assert preprefix[-1] == "run", "Issue with duration's parent"

        prefix_text = preprefix
        prefix_text[-2] = prefix_text[-2] + ".." + str(self.timekeeper.time + self.duration - Time(1))
        return " ".join(prefix_text)

    def end(self)-> list[str]:
        self.timekeeper.latest_time += self.duration
        return []