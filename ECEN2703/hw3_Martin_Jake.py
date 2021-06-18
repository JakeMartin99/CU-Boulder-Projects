#Jake Martin
#
#Z3's Solution: V is not guilty and W is guilty, or vice-versa
#Note: some characters' statements were simplified to logically equivalent but simpler statements.

#Imports all z3 libraries needed
from z3 import *

#Function to solve and print model
def solve_and_print(s):
    result = s.check()
    if result == sat:
        printm(s)
        b = block_model(s)
        if s.check(b) == unsat:
            print('unique solution')
        else:
            print('solution not unique')
            printm(s)
    elif result == unsat:
        print ('unsatisfiable')
    else:
        print('unsolvable')

#Function to block current solution
def block_model(s):
    q = s.model()
    return simplify( v != q[v] )
    #If v is not equal to its model, then w must be too because they are interchangable in H's statement,
    #so only one of the two must be blocked.
#Function to print
def printm(s):
    print(', '.join([str(x) + ' = ' + str(s.model()[x])
                         for x in [v, w]]))

a, b, c, d, e, f, g, h, v, w = [Bool(name) for name in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'v', 'w']]
s = Solver()

#A claims he is a knight
s.add(Implies(a, a))
#B is silent
#-----
#C claims A is a knave
s.add(Implies(c, Not(a)))
#D claims B is a knave
s.add(Implies(d, Not(b)))
#E claims C and D are both knights
s.add(Implies(e, And(c, d)))
#F claims a and/or b is a knight
s.add(Implies(f, Or(a, b)))
#G claims e and f are the same type
s.add(Implies(g, e==f))
#H claims g and h are the same type, AND that not v and w are both guilty
s.add(Implies(h, And((g==h), Not(And(v, w)) )))

solve_and_print(s)

