from basic_commands import MiCufunction_Command
from utils import Objective, Score_Holder

class Set(MiCufunction_Command):
    takes_block = False

    def __init__(self, stack, line, args) -> None:
        super().__init__(stack, line, args)
        self.objective = self.find_objective(stack)
        self.text = self.get_text(args)

    def get_text(self, args):
        if len(args) == 4:
            self.text = self.immediate_op(args)
        else:
            assert False, "Only immediates implemented yet"

        self.text = [self.add_prefix(line) for line in self.text]

    def immediate_op(self, args):
        simple_ops = ["=", "+=", "-="]
        complex_ops = ["*=", "/=", "%="]
        ops = simple_ops + complex_ops

        var1 = Score_Holder(args[1])
        assert args[2] in ops, "Unsupported immediate op"
        var2 = int(args[3])
        assert -2**31 <= var2 <= 2**31-1, "Integer must be signed 32 bit"

        # This is kind of unnecessary optimization
        # But it saves a line in the compiled .mcfunction
        if args[2] == "=":
            return [f"scoreboard players set {var1} {self.objective} {var2}"]
        elif args[2] == "+=" and var2 != -2147483648: # We can't negate this so fall back to unoptimized version
            if var2 >= 0:
                return [f"scoreboard players add {var1} {self.objective} {var2}"]
            else:
                return [f"scoreboard players remove {var1} {self.objective} {-var2}"]
        elif args[2] == "-=" and var2 != -2147483648:
            if var2 >= 0:
                return [f"scoreboard players remove {var1} {self.objective} {var2}"]
            else:
                return [f"scoreboard players add {var1} {self.objective} {-var2}"]
        else:
            return [
                f"scoreboard players set temp {self.objective} {var2}",
                f"scoreboard players operation {var1} {self.objective} {args[2]} {var2} {self.objective}"
            ]


                