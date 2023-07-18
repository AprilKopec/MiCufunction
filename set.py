from utils import MiCufunction_Command

class Set(MiCufunction_Command):
    takes_block = False

    def __init__(self, stack, line, args) -> None:
        self.objective = self.find_objective(stack)
        pass