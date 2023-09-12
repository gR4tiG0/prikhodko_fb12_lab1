#!/usr/bin/python3
from bignum import *
from Crypto.Random.random import getrandbits



BITS = 1024

TEST_NUMBER_A = getrandbits(BITS)
TEST_NUMBER_B = getrandbits(BITS)
e_ = "[!]"
d_ = "[*]"
q_ = "[?]"

def main() -> None:
    print(f"{d_} Testing number: {TEST_NUMBER_A}, base 2**64")
    big_A = bn(TEST_NUMBER_A)
    print(f"{e_} Number in new base: {big_A}")
    print(f"{e_} Number converted back to base 10: {big_A.base10()}")
    print(f"{q_} Here is hex with hex() from python:\n    {hex(TEST_NUMBER_A)}")
    print(f"{e_} And here is hex from library:\n    {big_A.baseN(16)}")
    print(f"{q_} Here is binary using bin() from python\n    {bin(TEST_NUMBER_A)}")
    print(f"{e_} And here is binary format from library:\n    {big_A.baseN(2)}")
    
    print(f"{d_} Sum using python:\n    A + B = {TEST_NUMBER_A+TEST_NUMBER_B}")
    big_B = bn(TEST_NUMBER_B)
    C = big_A + big_B

    # print("\n")
    # print(C)
    print("\n")
    print(bn(TEST_NUMBER_B+TEST_NUMBER_A))
if __name__ == "__main__":
    main()
