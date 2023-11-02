#!/usr/bin/python3
from compmath.bn import *
from random import getrandbits
from timeit import default_timer as timer
from secrets import randbelow
import sys
BITS = 1024
sys.set_int_max_str_digits(100000000)
def main() -> None:
    A,B,C,D = getrandbits(BITS),getrandbits(BITS),getrandbits(BITS),getrandbits(BITS//4)
    a,b,c,d = bn(A),bn(B),bn(C),bn(D)
    print((A+B)*C == ((a+b)*c).base10()) 
    print((A+B*C)*C == ((a+b*c)*c).base10()) 
    print((A//C+B*C)*C == ((a/c+b*c)*c).base10()) 
    print(C*(A//C+B*C) - A**2//B == (c*(a/c+b*c) - a**bn(2)/b).base10()) 
    print(C**3 == (c**bn(3)).base10())
    # nums = []
    # for _ in range(1000):
    #     A,B = getrandbits(BITS),getrandbits(BITS//2)
    #     assert (bn(A)%bn(B)).base10() == A%B
    # for _ in range(10):
    #     a.rshB()
    #     A = A >> 1
    #     assert a.base10() == A
    # a,b = bn(A),bn(B)
    # c = a/b
    # print(c.base10() == A//B)
    # start_time = timer()
    # for i in range(100):
    #     A,B = getrandbits(BITS),getrandbits(BITS)
    #     bn(A)/bn(B)
    # end_time = timer()
    # wbntime = end_time-start_time
    # print(f"{wbntime/100:.12f}")

    # for _ in range(100001):
    #     nums.append(bn(getrandbits(BITS)))
    # start_time = timer()
    # for i in range(100000):
    #     nums[i] / nums[i+1]
    # end_time = timer()
    # wbntime = end_time-start_time
    # print(f"{wbntime/100000:.12f}")
if __name__ == "__main__":
    main()