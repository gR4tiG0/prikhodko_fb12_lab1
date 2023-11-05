#!/usr/bin/python3
from compmath.bignum import *
from random import getrandbits
from timeit import default_timer as timer
BITS = 2048
def main() -> None:
    start_time = timer()
    for i in range(100):
        A,B = getrandbits(BITS),getrandbits(BITS//2)
        bn(A)/bn(B)
    end_time = timer()
    wbntime = end_time-start_time
    print(f"{wbntime/100:.12f}")
    # start_time = timer()
    # for _ in range(1000):
        # A = getrandbits(1024)
        # B = getrandbits(1024)
        # C = A+B
        # a = bn(A)
        # b = bn(B)
        # c = a+b
        # assert c.base10() == C
        # C = A*B
        # c = a*b
        #assert c.base10() == C
    # end_time = timer()
    # wbntime = end_time-start_time
    # start_time = timer()
    # for _ in range(1000):
        # A = getrandbits(1024)
        # B = getrandbits(1024)
        # C = A*B
    # end_time = timer()
    # wobntime = end_time-start_time
    # print(f"{wbntime/1000:.12f}")
    # print(f"{(wbntime-wobntime)/1000:.12f}")
if __name__ == "__main__":
    main()
