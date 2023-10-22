#!/usr/bin/python3
from compmath.bignum import *
from Crypto.Random.random import getrandbits
BITS = 1024

for _ in range(500):
    TEST_NUMBER_A = getrandbits(BITS)
    TEST_NUMBER_B = getrandbits(BITS)
    a = bn(TEST_NUMBER_A)
    b = bn(TEST_NUMBER_B)
    if (a*b).base10() != TEST_NUMBER_B*TEST_NUMBER_A:
        print(a,b)