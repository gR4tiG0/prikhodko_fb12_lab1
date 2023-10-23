#!/usr/bin/python3
from compmath.bignum import *
from Crypto.Random.random import getrandbits
from Crypto.Util.number import getPrime
import math
BITS = 1024

BASE_POWER = 16
TEST_NUMBER_A = getrandbits(BITS)
TEST_NUMBER_B = getrandbits(BITS)
TEST_NUMBER_C = getrandbits(BITS)
TEST_NUMBER_D = getPrime(BITS)
if TEST_NUMBER_A < TEST_NUMBER_B: TEST_NUMBER_B,TEST_NUMBER_A = TEST_NUMBER_A,TEST_NUMBER_B
MOD = getrandbits(BITS)
e_ = "[!]"
d_ = "[*]"
q_ = "[?]" 

def main() -> None:
    a = bn(TEST_NUMBER_A)
    b = bn(TEST_NUMBER_B)
    c = bn(TEST_NUMBER_C)
    #print(TEST_NUMBER_A,TEST_NUMBER_B)
    print(gcd(a,b).base10() == math.gcd(TEST_NUMBER_B,TEST_NUMBER_A))
    #print(lcm(a,b).base10() == math.lcm(TEST_NUMBER_B,TEST_NUMBER_A))
    gf = GF(MOD)
    a = gf(a)
    print((TEST_NUMBER_A-TEST_NUMBER_B)%MOD == (a-b).base10())
    print((TEST_NUMBER_A+TEST_NUMBER_B)%MOD == (a+b).base10())
    print((TEST_NUMBER_A*TEST_NUMBER_B)%MOD == (a*b).base10())
    print(((TEST_NUMBER_A+TEST_NUMBER_B)*TEST_NUMBER_C)%MOD == ((a+b)*c).base10() == (a*c + b*c).base10())
    gf = GF(TEST_NUMBER_D)

    C = getrandbits(25)
    print(C)
    mod = 11#getrandbits(16)
    c = bn(C)
    gf = GF(mod)
    c = gf(c)
    print((3**C)%mod == (gf(bn(3))**c).base10())
if __name__ == "__main__":
    main()


