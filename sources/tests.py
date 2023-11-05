#!/usr/bin/python3
from compmath.bn import *
from Crypto.Random.random import getrandbits
from secrets import randbelow
from timeit import default_timer as timer
e_,q_,a_ = "[!]","[?]","[*]"

def main() -> None:
    length = 2**1024
    BITS = 1024
    print(f"{a_} Checking the correctness of the convertion...")
    A = randbelow(length)
    Abn = bn(A)
    print(f"A == Abn: {A == Abn.base10()}")
    print(f"A16== Abn16: {hex(A)[2:] == Abn.baseN(16).lower()}")
    print(f"A2 == Abn2: {bin(A)[2:] == Abn.baseN(2)}")
    print(f"{e_} Convertion to common bases seeems right")
    print(f"{a_} Checking addition...")
    A,B,C,D = getrandbits(BITS), getrandbits(BITS), getrandbits(BITS//2), getrandbits(BITS)
    Abn,Bbn,Cbn,Dbn = bn(A),bn(B),bn(C),bn(D)
    R = Ring(C)
    Abn = R(Abn)
    print(f"A + B == Abn + Bbn (mod C): {(A+B)%C == (Abn+Bbn).base10()}")
    print(f"{e_} Addition seems right checking subtraction...")
    print(f"A - B == Abn - Bbn: {(A-B)%C == (Abn-Bbn).base10()}")
    print(f"{e_} Subtraction seems right")
    print(f"{a_} Checking multiplication...")
    print(f"A * B == Abn * Bbn: {(A*B)%C == (Abn*Bbn).base10()}")
    print(f"(Abn+Bbn)*Cbn == Abn*Cbn + Bbn*Cbn: {((Abn+Bbn)*Cbn).base10() == (Abn*Cbn + Bbn*Cbn).base10()}")
    print(f"{e_} Multiplication seems right")
    print(f"{a_} Checking power...")
    print(f"Abn**Bbn == A**B: {(Abn**bn(B)).base10() == pow(A,B,C)}")
    # print(f"{e_} Seems right")
    # print(f"{a_} Starting time tests")
    # r_numbers = []
    # for _ in range(10001): r_numbers.append(randbelow(length))
    # start_time = timer()
    # for i in range(len(r_numbers)-1):
    #     res = r_numbers[i] + r_numbers[i+1]
    # end_time = timer()
    # execution_time = (end_time - start_time)/10000
    # print(f"Average addition time: {execution_time:.12f} seconds")

    # start_time = timer()
    # for i in range(len(r_numbers)-1):
    #     res = r_numbers[i] - r_numbers[i+1]
    # end_time = timer()
    # execution_time = (end_time - start_time)/10000
    # print(f"Average subtraction time: {execution_time:.12f} seconds")

    # start_time = timer()
    # for i in range(len(r_numbers)-1):
    #     res = r_numbers[i] * r_numbers[i+1]
    # end_time = timer()
    # execution_time = (end_time - start_time)/10000
    # print(f"Average multiplication time: {execution_time:.12f} seconds")

    # start_time = timer()
    # for i in range(len(r_numbers)-1):
    #     res = r_numbers[i] / r_numbers[i+1]
    # end_time = timer()
    # execution_time = (end_time - start_time)/10000
    # print(f"Average division time: {execution_time:.12f} seconds")
    
    # base_l = [] 
    # for _ in range(10):base_l.append(getrandbits(4))
    # power_l = []
    # for _ in range(10): power_l.append(getrandbits(12))
    # start_time = timer()
    # for i in range(10):
    #     C = base_l[i] ** power_l[i]
    # end_time = timer()

    # execution_time = (end_time - start_time) / 10
    # print(f"Average powering time: {execution_time:.12f} seconds")
   
if __name__ == "__main__":
    main()
