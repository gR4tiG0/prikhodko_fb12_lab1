#!/usr/bin/python3
import cProfile
from random import getrandbits
from compmath.bignum import *

A,B,C,D,M = getrandbits(2048),getrandbits(2048),getrandbits(128),getrandbits(8),getrandbits(2048)
g = GF(M)
Abn,Bbn,Cbn,Dbn = g(bn(A)),g(bn(B)),g(bn(C)),g(bn(D))

def add():
    r = Abn + Bbn
def sub():
    r = Abn - Bbn
def mul():
    r = Abn * Bbn 
def pow():
    r = bn(3)**Dbn

def main() -> None:
    cProfile.run('add()')
    cProfile.run('sub()')
    cProfile.run('mul()')
    cProfile.run('pow()')
if __name__ == "__main__":
    main()