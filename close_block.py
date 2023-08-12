from conditional import Else
from command_baseclass import MiCufunction_Command

class Close_Block(MiCufunction_Command):
    can_pop_filename = True
    def __init__(self, stack, line, args) -> None:
        # Xero I am sorry
        self.pop_filename = False
        assert args == ["}"] or args == ["}","else","{"], "Incorrect usage of }"
        if line == "}":
            item = stack.pop()
            self.text = item.end()
            if type(item).has_filename:
                self.pop_filename = True

        elif line == "} else {":
            if_block = stack.pop()
            self.text = if_block.end(True)
            item = Else(if_block)
            self.text += item.begin()

            stack.append(item)
