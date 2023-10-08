from compmath.bignum import *
from Crypto.Random.random import getrandbits

A,B = getrandbits(256),getrandbits(256)
a,b = bn(A),bn(B)
print(A*B)
print((a*b).base10())
