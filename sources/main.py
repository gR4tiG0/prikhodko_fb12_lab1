#!/usr/bin/python3
from compmath.bn import *
from random import getrandbits
from timeit import default_timer as timer
from secrets import randbelow
import math
import sys
BITS = 2048
def main() -> None:
    # A,B,C = 107688068535652727143210867007033159873980637979636154602773282638412054626772451793848191833834714116369081928192729372447368971375826920905312732436878063700361283344995968371610253391808124886711354158658763659450686146100291242467468944267691173491961706675317397990619678117900392455483629777919890585461, 136202811676069604245549758792945451779207767187119645337511776981031544408410148211141958146099006477994534591295033701375042459414051062424827800959836594266196506899992910537613587341442901334614708053419315748918227204016640151402969006446506828068230434137770985052038472257227330520808676735014224856004, 171551503358636571352502408899151583282154415254305486164983585643621268317804837102746228961543293956929428196799945344040717696663984180548913083246844758743932574710444677043110006336836460086874935140020182198511658365182720994505341085648955857004858297093340600879578981501222714533943962032542098470597
    # a,b,c = bn(A),bn(B),bn(C)
    # Ring(C)
    # barrettReduction(a*b)
    # for i in range(10000):
    A,B,C = getrandbits(BITS),getrandbits(BITS),getrandbits(256)#4346908715 ,1910260801 ,8577061170#
    #     #print(A%C,B,C)
    #     A = A%C
    #     B = B%C
    #     # print(A*B > C**2)
    #     if A*B > C**2:
    #         exit()
    a,b,c = bn(A),bn(B),bn(C)
    #     # print(a*b > c**bn(2))
    #     R = Ring(C)
    #     # print(A,B,C)
    #     print(i,(A*B)%C == barrettReduction(a*b,c).base10())


    R = Ring(C)
    # print(A,B,C)
    a = R(a)
    res = (a**b).base10()
    print(res)
    print(pow(A,B,C))
    print(res == pow(A,B,C))
    # print((A+B)%C == (a+b).base10())
    # print((A-B)%C == (a-b).base10())
    # print((A*B)%C == (a*b).base10())
    # print((B**2)%C == (R(b)**bn(2)).base10())
    # print(A,B)
    # print("gcd",math.gcd(A,B))
    # print("Gcd",gcd(a,b).base10())
    # start_time = timer()
    # for i in range(1000):
    #     A,B = getrandbits(BITS),getrandbits(BITS)
    #     gcd(bn(A),bn(B))
    # end_time = timer()
    # wbntime = end_time-start_time
    # print(f"{wbntime/1000:.12f}")















    # A,B,C,D = getrandbits(BITS),getrandbits(BITS),getrandbits(BITS),getrandbits(BITS//4)
    # a,b,c,d = bn(A),bn(B),bn(C),bn(D)
    # print((A+B)*C == ((a+b)*c).base10()) 
    # print((A+B*C)*C == ((a+b*c)*c).base10()) 
    # print((A//C+B*C)*C == ((a/c+b*c)*c).base10()) 
    # print(C*(A//C+B*C) - A**2//B == (c*(a/c+b*c) - a**bn(2)/b).base10()) 
    # print(C**3 == (c**bn(3)).base10())
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