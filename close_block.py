from conditional import If
from command_baseclass import MiCufunction_Command
from utils import Time

class Close_Block(MiCufunction_Command):
    takes_block = False
    def __init__(self, stack, line, args) -> None:
        # Xero I am sorry
        assert args == ["}"] or args == ["}","else","{"], "Incorrect usage of }"
        if line == "}":
            self.item = stack.pop()
            self.text = self.item.end()

        elif line == "} else {":
            self.item = stack.pop()
            assert isinstance(self.item, If), "else must go after if"
            self.text = self.item.end()

            # We can't have both the If and the Else delay the cutscene by a tick
            # This is hacky and we should probably do something better
            self.item.parent.time += Time(-1) 

            condition = self.item.condition.split(" ")
            condition[1] = "unless"
            condition = " ".join(condition)
            self.item.condition = condition
            self.text += self.item.begin()

            stack.append(self.item)