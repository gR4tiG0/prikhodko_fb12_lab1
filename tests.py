#!/usr/bin/python3
from compmath.bignum import *
from Crypto.Random.random import getrandbits
from secrets import randbelow
from timeit import default_timer as timer
e_,q_,a_ = "[!]","[?]","[*]"

def main() -> None:
    length = 2**2048
    print(f"{a_} Checking the correctness of the convertion...")
    A = randbelow(length)
    Abn = bn(A)
    print(f"A == Abn: {A == Abn.base10()}")
    print(f"A16== Abn16: {hex(A)[2:] == Abn.baseN(16).lower()}")
    print(f"A2 == Abn2: {bin(A)[2:] == Abn.baseN(2)}")
    print(f"{e_} Convertion to common bases seeems right")
    print(f"{a_} Checking addition...")
    A,B,C,D = randbelow(length),randbelow(2**128),randbelow(length),-1*randbelow(length)
    Abn,Bbn,Cbn,Dbn = bn(A),bn(B),bn(C),bn(D)
    print(f"Abn + Bbn == Bbn + Abn: {Abn + Bbn == Bbn + Abn}")
    print(f"A + B == Abn + Bbn: {A+B == (Abn+Bbn).base10()}")
    print(f"(A + B) + C == Abn + (Bbn + Cbn): {A+B+C == (Abn+Bbn+Cbn).base10()}")
    print(f"D + A == Dbn + Abn, where D is negative number: {D + A == (Dbn + Abn).base10()}")
    print(f"{e_} Addition seems right checking subtraction...")
    print(f"Abn - Bbn == Bbn - Abn: {Abn - Bbn == Bbn - Abn}")
    print(f"A - B == Abn - Bbn: {A-B == (Abn-Bbn).base10()}")
    print(f"(A - B) - C == Abn - (Bbn - Cbn): {A-B-C == (Abn-Bbn-Cbn).base10()}")
    print(f"D -  A == Dbn - Abn, where D is negative number: {D - A == (Dbn - Abn).base10()}")
    print(f"{e_} Subtraction seems right")
    print(f"{a_} Checking multiplication...")
    print(f"Abn - Bbn == Bbn - Abn: {Abn * Bbn == Bbn * Abn}")
    print(f"A - B == Abn - Bbn: {A*B == (Abn*Bbn).base10()}")
    print(f"(A - B) - C == Abn - (Bbn - Cbn): {A*B*C == (Abn*Bbn*Cbn).base10()}")
    r = bn(0)
    for _ in range(123): r = r + Abn
    print(f"Abn * 123 = Abn+Abn...+Abn times 123: {(Abn * bn(123)).base10() == (r.base10())}")
    print(f"(Abn+Bbn)*Cbn == Abn*Cbn + Bbn*Cbn: {((Abn+Bbn)*Cbn).base10() == (Abn*Cbn + Bbn*Cbn).base10()}")
    print(f"{e_} Multiplication seems right")
    print(f"{a_} Checking division...")
    print(f"Abn > Bbn: {Abn > Bbn}")
    print(f"Abn // Bbn == A // B: {(Abn / Bbn).base10() == A//B}")
    print(f"Abn < Bbn: {Abn < Bbn}")
    print(f"Bbn // Abn == B // A: {(Bbn / Abn).base10() == B//A}")
    print(f"Abn % Bbn == A % B: {(Abn % Bbn).base10() == A%B}")
    print(f"{e_} Division seems right")
    print(f"{a_} Checking power...")
    base = getrandbits(4)
    power = getrandbits(12)
    k = 3**power
    print(f"base**Bbn == base**B: {(bn(3)**bn(power)).base10() == k}")
    print(f"{e_} Seems right")
    print(f"{a_} Starting time tests")
    r_numbers = []
    for _ in range(10001): r_numbers.append(randbelow(length))
    start_time = timer()
    for i in range(len(r_numbers)-1):
        res = r_numbers[i] + r_numbers[i+1]
    end_time = timer()
    execution_time = (end_time - start_time)/10000
    print(f"Average addition time: {execution_time:.12f} seconds")

    start_time = timer()
    for i in range(len(r_numbers)-1):
        res = r_numbers[i] - r_numbers[i+1]
    end_time = timer()
    execution_time = (end_time - start_time)/10000
    print(f"Average subtraction time: {execution_time:.12f} seconds")

    start_time = timer()
    for i in range(len(r_numbers)-1):
        res = r_numbers[i] * r_numbers[i+1]
    end_time = timer()
    execution_time = (end_time - start_time)/10000
    print(f"Average multiplication time: {execution_time:.12f} seconds")

    start_time = timer()
    for i in range(len(r_numbers)-1):
        res = r_numbers[i] / r_numbers[i+1]
    end_time = timer()
    execution_time = (end_time - start_time)/10000
    print(f"Average division time: {execution_time:.12f} seconds")
    
    base_l = [] 
    for _ in range(10):base_l.append(getrandbits(4))
    power_l = []
    for _ in range(10): power_l.append(getrandbits(12))
    start_time = timer()
    for i in range(10):
        C = base_l[i] ** power_l[i]
    end_time = timer()

    execution_time = (end_time - start_time) / 10
    print(f"Average powering time: {execution_time:.12f} seconds")
   
if __name__ == "__main__":
    main()
