from compmath.bignum import *

def status(inp):
    for i in inp:
        print(i.base10(),end=" ")
    print("")

A,B,C,D = bn(-3),bn(-5),bn(3),bn(5)
print(f"{A.base10()} - {B.base10()} = {(A - B).base10()}")
status([A,B,C,D])
