from utils import Time

class Duration:
    takes_block = True
    def __init__(self, stack, line, args) -> None:
        self.parent = stack[-1]
        self.duration = Time(args[1])
        self.text = self.begin()

    def begin(self) -> list[str]:
        return []

    def prefix(self) -> str:
        preprefix = self.parent.prefix().split()
        
        # This is almost certainly not the correct way to do this
        assert preprefix[-5] == "if", "Issue with duration's parent"
        assert preprefix[-3] == "matches", "Issue with duration's parent"
        assert preprefix[-2].isdigits() or (preprefix[-2][0] == '-' and preprefix[-2][1:].isdigits()), "Issue with duration's parent"
        assert preprefix[-1] == "run", "Issue with duration's parent"

    def end(self)-> list[str]:
        return []