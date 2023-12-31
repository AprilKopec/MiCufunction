from utils import Score_Holder, Objective, Scope
from itertools import product

class Execute_Condition_Atom:
    def __init__(self, condition: str):
        self.condition = " ".split(condition,1)
        assert self.condition[0] in ["if", "unless"], ValueError("Conditional execution subcommands must begin with 'if' or 'unless'.")
        
    def __invert__(self):
        if self.condition[0] == "if":
            return ["unless", self.condition[1]]
        else:
            return ["if", self.condition[1]]
        
    def __str__(self):
        return " ".join(self.condition)

class Execute_Condition:
    # This class contains a boolean algebraic combination of atoms in disjunctive normal form
    # self.conditions is a set of sets of atoms; the inner sets are ANDed, and then the outer sets are ORed.
    def __init__(self, arg, scope = None):
        if isinstance(arg, str):
            self.conditions = self.evaluate(arg, scope).conditions
        elif isinstance(arg, list[list[Execute_Condition_Atom]]):
            self.conditions = arg
        elif isinstance(arg, Execute_Condition_Atom):
            self.conditions = [[arg]]
        else:
            raise ValueError("Execute_Condition must be initialized with a string or a DNF expression of atomic execute conditions.")

    def evaluate(self, expression: str, scope: Scope):
        # This can plausibly break if you have a string with ~()&| in it in NBT in a literal
        # I don't anticipate that coming up, and if it does we can just define a variable and then use it instead of making a literal
        expression = expression.strip()
        # Case 1: Stuff we need to count parens for: expression in parens, &, or |
        # This is left associative, but please just use parens 
        if expression[0] == "(" or "&" in expression or "|" in expression:
            paren_bal: int = 0
            for i in len(" ".split(expression)):
                if expression[i] == "(":
                    paren_bal += 1
                elif expression[i] == ")":
                    paren_bal -= 1
                elif expression[i] == "&" and paren_bal == 1:
                    return Execute_Condition(expression[1:i], scope) & Execute_Condition(expression[i+1:], scope)
                elif expression[i] == "|" and paren_bal == 1:
                    return Execute_Condition(expression[1:i], scope) | Execute_Condition(expression[i+1:], scope)
                else:
                    continue
            if not paren_bal == 0:
                raise ValueError("Execute_Condition expression has unbalanced parentheses")
            else:
                return Execute_Condition(expression[1:-1], scope)
        # Case 2: Inverted expression. You're welcome future April for making &| take precedence over ~
        if expression[0] == "~":
            return ~Execute_Condition(expression[1:], scope)
        # Case 3: The expression is a named variable
        elif expression in scope:
            return scope[expression]
        # Case 4: The expression is an atomic condition
        else:
            try:
                return Execute_Condition(Execute_Condition_Atom(expression))
            except:
                raise ValueError("Issue with syntax in Execute_Condition expression")
            
            

    def __or__(self, other) -> [list]:
        # This is easy, just concatenate the disjunctions
        return Execute_Condition(self.conditions + other.conditions)
    
    def __and__(self, other):
        # ((p & q) | (r & s)) & ((x & y) | (z & w))
        # <-> ((p & q & x & y) | (p & q & z & w) | (r & s & x & y) | (r & s & z & w))
        # For both disjunctions to be true, one conjunction from each must be true
        # So the conjunctions in the result consist of one conjunction from each disjunction, appended together
        return Execute_Condition([[a + b for b in other.conditions] for a in self.conditions])
    
    def __invert__(self) -> [list]:
        # ~((x & y) | (z & w))
        # <-> ((~x & ~z) | (~x & ~w) | (~y & ~z) | (~y & ~w))
        # For the disjunction to be false, each conjunction must be false
        # So one variable from each conjunction must be false
        # So the conjunctions in the inverse consist of the inverse of one variable from each original conjunction
        inverted_atoms = [[~x for x in conjunction] for conjunction in self.conditions]
        return Execute_Condition([list(conjunction) for conjunction in product(*inverted_atoms)])
    
    def commands(self, score_holder: Score_Holder, objective: Objective) -> list[str]:
        text = [f'scoreboard players set {score_holder} {objective} 0']
        text += [f'execute {" ".join(conjunction)} run scoreboard players set {score_holder} {objective} 1' for conjunction in self.conditions]