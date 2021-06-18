#Jake Martin
#
#Output: Valid
#
from z3  import *

def  solve_and_print(s):
    result = s.check()
    if result == s.check():
        if s.check() == unsat:
            print('Valid') # Tautology because negation is unsat
        else:
            print('Not valid') # Not tautology because negation is sat
    else:
        print('Z3 couldn\'t solve it')

x, y, z = [Int(name) for  name in ['x', 'y', 'z']]

s = Solver ()
q = ForAll(x, Exists(y, And(x < y, ForAll(z, Or(x >= z, z >= y) ) ) ) ) 
s.add(Not(q))
solve_and_print(s)