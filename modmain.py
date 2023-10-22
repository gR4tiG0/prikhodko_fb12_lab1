#!/usr/bin/python3
from compmath.bignum import *
from Crypto.Random.random import getrandbits
import math
BITS = 1024

BASE_POWER = 16
TEST_NUMBER_A = getrandbits(BITS)
TEST_NUMBER_B = getrandbits(BITS)

e_ = "[!]"
d_ = "[*]"
q_ = "[?]" 

def main() -> None:
    a = bn(TEST_NUMBER_A)
    b = bn(TEST_NUMBER_B)
    print(gcd(a,b).base10() == math.gcd(TEST_NUMBER_B,TEST_NUMBER_A))
    print(lcm(a,b).base10() == math.lcm(TEST_NUMBER_B,TEST_NUMBER_A))


if __name__ == "__main__":
    main()

