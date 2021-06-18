"""
Jake Martin
HW 12 Problem 4
Find first 12 digit prime in e
"""

from sympy import isprime
from mpmath import mp

decimalPlaces = 100
with mp.workdps(decimalPlaces):
    estring = str(mp.e).replace('.','')

print("\ne:", estring, '\n')

for i in range(len(estring)):
    esect = int(estring[i:i+12])
    if isprime(esect):
        break;

print("Answer:", esect, '\n')
print("Starting at digit index:", i)
