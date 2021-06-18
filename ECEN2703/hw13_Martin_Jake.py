#Jake Martin
#
#Output: 84 4-colorings
#

from z3  import *
from typing import List, Set
Graph = List[Set[int]]
VarList = List[ArithRef]

def Chromatic(G: Graph, k: int): #-> Optional[Coloring]:
    """Finds k-coloring of G"""
    n = len(G)
    verts = [Int('%i' % i) for i in range(n)]
    s = Solver()
    s.add([And(x>=0, x<k) for x in verts])
    for i in range(n):
        s.add([verts[i] != verts[j] for j in G[i]])
    if s.check() == sat:
        m = s.model()
        print([m[x].as_long() for x in verts])
        count = 1
        Add(s, verts)
        while s.check() == sat:
            count += 1
            #print([s.model()[x].as_long() for x in verts])
            Add(s, verts)
        else:
            print("That's it")
        return count
    else:
        return 0

def Add(s, verts):
    m = s.model()
    s.add(Or(verts[0] != m[verts[0]],
             Or(verts[1] != m[verts[1]],
                Or(verts[2] != m[verts[2]],
                   verts[3] != m[verts[3]]) ) ) )

Square = ( {1, 3}, {0, 2}, {1, 3}, {0, 2} )
for k in range(0, 9):
    print(str(k) + "-colorings:")
    print("Quantity: ", Chromatic(Square, k), "\n") 
