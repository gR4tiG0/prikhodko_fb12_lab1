#!/usr/bin/python3
from math import log

class bn:
    """Class for working with large numbers"""


    def __init__(self, number):
        self.Bp = 64
        self.base = 2**self.Bp
        self.length = int(log(number,self.base))
        
        if number == 0: self.n = [0]
        else:
            digits = []
            while number > 0:
                remainder = number % self.base
                digits.append(remainder)
                number = number // self.base
            digits.reverse()

            self.number = digits

    def __str__(self):
        return ", ".join([str(item) for item in self.number])

    def __repr__(self):
        """For ipython"""
        return self.number

    def __add__(self, other):
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
        num = 0 
        print(result)
        for digit in result: num = num * self.base + digit
        return bn(num)


    def base10(self) -> int:
        res = 0
        for digit in self.number:
            res = res * self.base + digit
        return res
    
    def baseN(self, base:int) -> str:
        if base > 16: 
            print("Invalid base. Please choose base < 16")
            return None
        elif base == 10:
            return self.base10()
        HEX_DIGITS = "0123456789ABCDEF"
        res = ""
        n = self.base10()
        while n > 0:
            remainder = n % base 
            res = HEX_DIGITS[remainder] + res
            n = n // base
        return res

    
