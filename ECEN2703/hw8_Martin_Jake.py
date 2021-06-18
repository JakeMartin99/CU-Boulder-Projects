#Jake Martin
#
#Prints True for subsets that need to be used for optimal cover, false for others
#

from z3  import *

def set_cover(collec):
    a = 0
    X = [Bool("x" + str(i)) for i in range(len(collec))]
    opt = Optimize()
    opt.minimize(Sum([If(v, 1, 0) for v in X]))
    while(True):
        lista = []
        for s in range(len(collec)):
            if a in collec[s]:
                lista.append(X[s])
        
        if len(lista) == 0:
            break
        opt.add(Or(lista))
        opt.check()
        a += 1
    mod = opt.model()
    mstr = str(mod)
    return mstr

if __name__ == '__main__':
    Ca = [{0,10}, {0,1,4}, {1,2,4,5,6,7}, {0,1,3,5,9},
          {0,3}, {2,6,8,11}, {2,7,8,10}, {3,9}]
    print(set_cover(Ca))