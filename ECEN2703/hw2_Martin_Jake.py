#Jake Martin
#
#The only solution is a=False, which means Alex must be a knave, and that his mom's status is indeterminable
#

#Imports all z3 libraries needed
from z3 import *

#Function to solve and print model
def solve_and_print(s):
    result = s.check()
    if result == sat:
        printm(s)
        b = block_model(s)
        print(b)
        if s.check(b) == unsat:
            print('unique solution')
        else:
            print('solution not unique')
            print(s.model())
    elif result == unsat:
        print ('unsatisfiable')
    else:
        print('unsolvable')

#Function to block current solution
def block_model(s):
    q = s.model()
    return simplify(a != q[a])

#Function to print
def printm(s):
    print(', '.join([str(x) + ' = ' + str(s.model()[x])
                         for x in [a, m]]))

s = Solver()
a = Bool('a') # a (Alex) is a truthful knight
m = Bool('m') # m (Alex's mom) is a truthful knight

# a says, "m said we aren't the same type"
s.add( Implies(a, ( m == (Not(a == m)) ) ) ) #Implication or bi-directional-implication?

solve_and_print(s)

