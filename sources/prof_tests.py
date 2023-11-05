#!/usr/bin/python3
import cProfile
from random import getrandbits
from compmath.bn import *

A,B,C = getrandbits(2048),getrandbits(2048),getrandbits(1024)
Abn,Bbn,Cbn = bn(A),bn(B),bn(C)
R = Ring(C)
Abn = R(Abn)
def add():
    r = Abn + Bbn
def sub():
    r = Abn - Bbn
def mul():
    r = Abn * Bbn 
def pow():
    r = Abn**Bbn

def main() -> None:
    cProfile.run('pow()')
    cProfile.run('add()')
    cProfile.run('sub()')
    cProfile.run('mul()')
if __name__ == "__main__":
    main()