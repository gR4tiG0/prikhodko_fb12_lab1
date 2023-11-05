#!/usr/bin/python3
import cProfile
from random import getrandbits
from compmath.bignum import *

A,B,C,D = getrandbits(2048),getrandbits(2048),getrandbits(128),getrandbits(8)
Abn,Bbn,Cbn,Dbn = bn(A),bn(B),bn(C),bn(D)

def add():
    r = Abn + Bbn
def sub():
    r = Abn - Bbn
def mul():
    r = Abn * Bbn 
def div():
    r = Abn / Cbn
def pow():
    r = bn(3)**Dbn

def main() -> None:
    cProfile.run('add()')
    cProfile.run('sub()')
    cProfile.run('mul()')
    cProfile.run('div()')
    cProfile.run('pow()')
if __name__ == "__main__":
    main()