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
        sign = 1
        if self.sign == -1:
            if other.sign == -1:
                sign = -1
            else:
                a = bn(self.number)
                return other.__sub__(a)
        elif other.sign == -1:
            a = bn(other.number)
            return self.__sub__(a)
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
        result = bn(result)
        result.sign = sign
        return result

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
        if self.sign == -1:
            if other.sign == -1:
                a = bn(self.number)
                b = bn(other.number)
                return b.__sub__(a)
            else:
                a = bn(self.number)
                res = a.__add__(other)
                res.sign = -1
                return res
        elif other.sign == -1:
            a = bn(other.number)
            return self.__add__(a)
        result,borrow = self.sub_s(other)
        if borrow != 0: 
            sign = -1
            result = other.__sub__(self)
            result.sign = sign 
            return result
        else: 
            return bn(result)

    def __ge__(self,other):
        _,borrow = self.sub_s(other)
        if borrow != 0:
            return False
        else:
            return True
    def __le__(self,other):
        _,borrow = other.sub_s(self)
        if borrow != 0:
            return False
        else:
            return True
    def __gt__(self,other):
        _,borrow = self.sub_s(other)
        if borrow != 0 or self.__eq__(other):
            return False
        else:
            return True
    def __lt__(self,other):
        _,borrow = other.sub_s(self)
        if borrow != 0 or self.__eq__(other):
            return False
        else:
            return True

    def __eq__(self,other):
        if self.number == other.number:
            return True
        else: 
            return False
    
    def mulStep(self, number):
        carry = 0
        result = []
        for a_d in self.number:
            tmp = a_d * number + carry
            result.append(tmp & (self.base - 1))
            carry = tmp >> self.Bp 
        result.append(carry)
        return result

    def shiftLeft(self, number, t):
        return [0]*t + number


    def __mul__(self, other):
        #default multiplication
        # result = bn(0)
        # for c,b_d in enumerate(other.number):
            # tmp = self.mulStep(b_d)
            # tmp = self.shiftLeft(tmp,c)
            # result = result + bn(tmp)

        #karatsuba variant
        result = self.karatsuba(other)
        return result
    
    def karatsubaStep(self,a,b):
        if a.length == 1 or b.length == 1:
            return bn(a.number[0] * b.number[0])
        else:
            n = max(a.length,b.length)
            m = n // 2
            a = a.number 
            b = b.number
            a_l,a_h = bn(a[:m]),bn(a[m:])
            b_l,b_h = bn(b[:m]),bn(b[m:])
            z0 = self.karatsubaStep(a_h,b_h)
            z2 = self.karatsubaStep(a_l,b_l)
            z1 = self.karatsubaStep(a_l,b_h) + self.karatsubaStep(a_h,b_l)
            z0_f = bn(self.shiftLeft(z0.number,n))
            z1_f = bn(self.shiftLeft(z1.number,m))

            z = z0_f + z1_f + z2
            return z



    def karatsuba(self,other):
        result = self.karatsubaStep(self,other)
        return result

    def __pow__(self,power):
        if power == 2:
            return self.karatsubaStep(self,self)
        else:
            return None
    
    def bitLength(self,number):
        return len(number.baseN(2))
    
    def shiftBitsL(self,number,n):
        number_ = number.baseN(2)
        number_ = "0"*(self.Bp - (n%self.Bp)) + number_ + n*"0"
        assert len(number_) % 64 == 0 
        digits = [int(number_[i:i+64],2) for i in range(0,len(number_),64)]
        digits.reverse()
        if set(digits) == {0}: digits = [0]
        return bn(digits)

    def shiftBitsH(self,number,n):
        number_ = number.baseN(2)
        number_ =  "0"*n + number_[:-n] 
        assert len(number_) % 64 == 0 
        digits = [int(number_[i:i+64],2) for i in range(0,len(number_),64)]
        digits.reverse()
        if set(digits) == {0}: digits = [0]
        return bn(digits)


    def divMod(self,other):
        if other.number == [0]:
            return None
        elif self == other:
            return 1
        elif self < other:
            return 0, self
        else:
            B = bn(self.number)
            A = bn(other.number)
            c = 1 
            while A <= B:
                A = self.shiftBitsL(A,1)
                c = c << 1
            c = c >> 1
            res = bn(0)
            A = self.shiftBitsH(A,1)
            c = bn(c)
            while not (c == bn(0)):
                if B >= A:
                    B = B - A
                    res = res + c
                c = self.shiftBitsH(c,1)
                A = self.shiftBitsH(A,1)
            return res,B


    def __truediv__(self,other):
        return self.divMod(other)[0]


    def __mod__(self,other):
        return self.divMod(other)[1]









