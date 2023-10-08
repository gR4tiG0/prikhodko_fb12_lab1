#!/usr/bin/python3
from compmath.bignum import *
from Crypto.Random.random import getrandbits
from secrets import randbelow

e_,q_,a_ = "[!]","[?]","[*]"

def main() -> None:
    length = 2^2048
    print(f"{a_} Checking the correctness of the convertion...")
    A = randbelow(length)
    Abn = bn(A)
    print(f"A == Abn: {A == Abn.base10()}")
    print(f"A16== Abn16: {hex(A)[2:] == Abn.baseN(16).lower()}")
    print(f"A2 == Abn2: {bin(A)[2:] == Abn.baseN(2)}")
    print(f"{e_} Convertion to common bases seeems right")
    print(f"{a_} Checking addition...")
    A,B,C,D = randbelow(length),randbelow(length),randbelow(length),-1*randbelow(length)
    Abn,Bbn,Cbn,Dbn = bn(A),bn(B),bn(C),bn(D)
    print(f"Abn + Bbn == Bbn + Abn: {Abn + Bbn == Bbn + Abn}")
    print(f"A + B == Abn + Bbn: {A+B == (Abn+Bbn).base10()}")
    print(f"(A + B) + C == Abn + (Bbn + Cbn): {A+B+C == (Abn+Bbn+Cbn).base10()}")
    print(f"D + A == Dbn + Abn, where D is negative number: {D + A == (Dbn + Abn).base10()}")
    print(f"{e_} Addition seems right checking subtraction...")
    print(f"Abn - Bbn == Bbn - Abn: {Abn - Bbn == Bbn - Abn}")
    print(f"A - B == Abn - Bbn: {A-B == (Abn-Bbn).base10()}")
    print(f"(A - B) - C == Abn - (Bbn - Cbn): {A-B-C == (Abn-Bbn-Cbn).base10()}")
    print(f"D - A == Dbn - Abn, where D is negative number: {D - A == (Dbn - Abn).base10()}")



if __name__ == "__main__":
    main()
