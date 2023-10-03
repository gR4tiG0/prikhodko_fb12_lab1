from compmath.conv_types import *
from math import log
BASE = 2
BASE_POWER = 64 
HEX_DIGITS = "0123456789ABCDEF"

class bn:
    """init class for operations with large numbers"""

    def __init__(self,number):
        self.Bp = BASE_POWER 
        self.base = BASE ** BASE_POWER
        digits,sign = convert(number,self.base)
        self.number = digits
        self.sign = sign
        self.length = len(self.number)
    
    def __str__(self):
        return ", ".join([str(item) for item in self.number])
    
    def __repr__(self):
        """for ipython3"""
        return ",".join([str(item) for item in self.number])

    def base10(self) -> int:
        res = 0
        for digit in self.number[::-1]:
            res = res * self.base + digit
        return res * self.sign
    
    def baseN(self,baseN:int):
        if baseN not in [2,10,16]:
            raise TypeError("Invalid convertion base or not implemented yet")
        if baseN == 10:
            return self.base10()
        res = ""
        for item in self.number:
            res_t = ""
            while item > 0:
                remainder = item % baseN
                res_t = HEX_DIGITS[remainder] + res_t
                item = item // baseN
            mod = (self.Bp // int(log(baseN,BASE)))
            rem = mod - len(res_t) 
            res_t = "0"*rem + res_t
            res = res_t + res
        return res if self.sign == 1 else "-" + res
