from compmath.conv_types import *

BASE = 2
BASE_POWER = 64

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
    
