# Jake Martin
# Order numbers 1-N such that consecutives sum to perfect squares
#
# Z3 Solution for N = 17: x1 = 17, x2 = 8, x3 = 1, x4 = 15, x5 = 10, x6 = 6, x7 = 3, x8 = 13, x9 = 12, x10 = 4, x11 = 5, x12 = 11, x13 = 14, x14 = 2, x15 = 7, x16 = 9, x17 = 16
# Z3 Solution for N = 18: Unsatisfiable (as expected)

from z3 import *
import math

#Function to solve and print model
def solve_and_print(s, X):
    result = s.check()
    if result == sat:
        printm(s, X)
    elif result == unsat:
        print ('unsatisfiable')
    else:
        print('unsolvable')

#Function to print
def printm(s, X):
    print(', '.join([str(x) + ' = ' + str(s.model()[x])
                         for x in X]))
    
#Function to model the repeated-or operation
def rep_or(S, X, i, m):
    ors = []
    for j in range(0, m-1):
        a = X[i] + X[i+1] == S[j]
        b = X[i] + X[i+1] == S[j+1]
        ors.append( Or(a, b) )
    
    while len(ors) > 1:
        ors[0] = Or(ors[0], ors[1])
        for i in range(1, len(ors)-1):
            ors[i] = ors[i+1]
        del ors[len(ors)-1]
        
    return ors[0]

#Read optional command line argument
import sys
if len(sys.argv) > 2:
    raise SystemExit("There should be at most one argument")
elif len(sys.argv) == 2:
    try:
        N = int(sys.argv[1])
    except:
        raise SystemExit("N should be an integer")
    if N < 0:
        raise SystemExit("N should be non-negative")
else:
    N = 15 #default value
print("For N=" + str(N) + ", ")

#Create X to hold N Int() variables
X = [Int('x'+ str(num+1)) for num in range(N)]

s = Solver()

#Adds the constraint that all of the variables are between 1 and N
for i in X:
    s.add(And(i >= 1, i <= N))
#Adds the constraint that all of the variables are unique
#for i in range(len(X)-1):
 #   s.add(Distinct(X[i], X[i+1]))
s.add(Distinct(X))
#Adds the constraint that each pair of consecutive variables must sum to a perfect square
S = [0]*int(math.sqrt(2*N)+1)
m = len(S)
for i in range(m):
    a = i * i
    S[i] = a
    if (i+1)*(i+1) > 2*N:
        break
print("Squares less than 2N: " + str(S))
for i in range(1, N):
    s.add(rep_or(S, X, i-1, m))

solve_and_print(s, X)
