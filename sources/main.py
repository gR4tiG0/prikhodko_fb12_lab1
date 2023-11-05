#!/usr/bin/python3
from compmath.bn import *
from random import getrandbits
from timeit import default_timer as timer
from secrets import randbelow
import math
import sys
BITS = 2048
def main() -> None:
    nums = []
    time_n = 100
    R = Ring(getrandbits(BITS//2))
    for _ in range(time_n+1):
        nums.append(R(bn(getrandbits(BITS))))

    start_time = timer()
    for i in range(time_n):
        nums[i] + nums[i+1]
    end_time = timer()
    wbntime = end_time-start_time
    print(f"Add: {wbntime/time_n:.12f}")

    start_time = timer()
    for i in range(time_n):
        nums[i] - nums[i+1]
    end_time = timer()
    wbntime = end_time-start_time
    print(f"Sub: {wbntime/time_n:.12f}")

    start_time = timer()
    for i in range(time_n):
        nums[i] * nums[i+1]
    end_time = timer()
    wbntime = end_time-start_time
    print(f"Mul: {wbntime/time_n:.12f}")

    start_time = timer()
    for i in range(time_n):
        nums[i] ** nums[i+1]
    end_time = timer()
    wbntime = end_time-start_time
    print(f"Pow: {wbntime/time_n:.12f}")

if __name__ == "__main__":
    main()