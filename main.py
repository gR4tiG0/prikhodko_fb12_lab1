#!/usr/bin/python3
from compmath.bignum import *
from Crypto.Random.random import getrandbits
BITS = 1024

TEST_NUMBER_A = -1 * getrandbits(BITS)
TEST_NUMBER_B = getrandbits(BITS)

e_ = "[!]"
d_ = "[*]"
q_ = "[?]" 

def main() -> None:
    A = bn(str(TEST_NUMBER_A))
    print(A)
    print(A.base10())
    print(TEST_NUMBER_A == A.base10())




if __name__ == "__main__":
    main()
