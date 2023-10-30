#!/usr/bin/python3
from compmath.bn import *
from random import getrandbits
from timeit import default_timer as timer

def main() -> None:
    start_time = timer()
    for _ in range(1000):
        A = getrandbits(1024)
        B = getrandbits(1024)
        # C = A+B
        a = bn(A)
        b = bn(B)
        # c = a+b
        # assert c.base10() == C
        # C = A-B
        # c = a-b
        # assert c.base10() == C
        c = a*b
        C = A*B
        # assert c.base10() == C
    end_time = timer()
    wbntime = end_time-start_time
    start_time = timer()
    for _ in range(1000):
        A = getrandbits(1024)
        B = getrandbits(1024)
        C = A*B
    end_time = timer()
    wobntime = end_time-start_time
    print(f"{wbntime/1000:.12f}")
    print(f"{(wbntime-wobntime)/1000:.12f}")
if __name__ == "__main__":
    main()