from conditional import If

class Close_Block:
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

            condition = self.item.condition.split(" ")
            condition[1] = "unless"
            condition = " ".join(condition)
            self.item.condition = condition
            self.text += self.item.begin()

            stack.append(self.item)

        
    def prefix(self):
        return self.item.prefix()