#!/usr/bin/python3
from compmath.bignum import *
from Crypto.Random.random import getrandbits
BITS = 2048 

BASE_POWER = 16
TEST_NUMBER_A = -1 * getrandbits(BITS)
TEST_NUMBER_B = getrandbits(BITS)

e_ = "[!]"
d_ = "[*]"
q_ = "[?]" 

def main() -> None:
    A = bn(TEST_NUMBER_A)
    print(A.base10() == TEST_NUMBER_A)
    print(int(A.baseN(16),16) == TEST_NUMBER_A)    
    print(int(A.baseN(2),2) == TEST_NUMBER_A)

if __name__ == "__main__":
    main()
