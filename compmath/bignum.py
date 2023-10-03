from compmath.conv_types import *
from math import log
BASE = 2
BASE_POWER = 64 
HEX_DIGITS = "0123456789ABCDEF"

class bn:
    """init class for operations with large numbers"""

    def __init__(self,number,sign=0):
        self.Bp = BASE_POWER 
        self.base = BASE ** BASE_POWER
        if sign != 0: digits,_ = convert(number,self.base)
        else: digits,sign = convert(number,self.base)
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


    def __add__(self,other):
        result = []
        carry = 0 
        m_len = max(self.length, other.length)
        for i in range(m_len):
            a_d = self.number[i] if i < len(self.number) else 0 
            b_d = other.number[i] if i < len(other.number) else 0 
            tmp = a_d + b_d + carry 
            carry = tmp // self.base        
            result.append(tmp % self.base)
        if carry > 0: result.append(carry)
        return bn(result)

    def sub_s(self,other):
        result = []
        borrow = 0 
        m_len = max(self.length, other.length)
        for i in range(m_len):
            a_d = self.number[i] if i < len(self.number) else 0 
            b_d = other.number[i] if i < len(other.number) else 0 
            tmp = a_d - b_d - borrow 
            if tmp >= 0:
                result.append(tmp)
                borrow = 0 
            else:
                result.append(tmp + self.base)
                borrow = 1 
        return result, borrow

    def __sub__(self,other):
        result,borrow = self.sub_s(other)
        if borrow != 0: 
            sign = -1
            result = other.__sub__(self)
            result.sign = sign 
            return result
        else: 
            return bn(result)

    def __gt__(self,other):
        _,borrow = self.sub_s(other)
        if borrow != 0:
            return False
        else:
            return True
    def __lt__(self,other):
        _,borrow = other.sub_s(self)
        if borrow != 0:
            return False
        else:
            return True
    
    def __eq__(self,other):
        if self.number == other.number:
            return True
        else: 
            return False
