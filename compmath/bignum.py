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
        res = res.lstrip('0')
        if res == '': res = '0'
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

    


    def __mul__(self, other):
        #default multiplication
        result = bn(0)
        for c,b_d in enumerate(other.number):
            tmp = self.mulStep(b_d)
            tmp = shiftLeft(tmp,c)
            result = result + bn(tmp)

        #karatsuba variant
        # n = max(self.length,other.length)
        # if n%2 != 0: n += 1
        # a = bn(self.number + [0]*(n-self.length))
        # b = bn(other.number + [0]*(n-other.length))
        #print(a)
        #print(b)
        # result = karatsubaStep(a,b)
        return result
    



    def __pow__(self,power):
        if power == bn(0):
            return bn(1)
        elif power == bn(1):
            return self
        elif power == bn(2):
            return self.__mul__(self)
        else:
            A,B,C = bn(self.number),bn(power.number),bn(1)
            D = [A]
            b_2 = B.baseN(2)
            b_2 = b_2[b_2.find('1'):]
            #print(b_2)
            for i in range(1,len(b_2),1):
                #print(f"prev: {D[i-1].base10()}")
                D.append(D[i-1] * D[i-1])
            #for i in D: print(i.base10())
            for c,i in enumerate(b_2[::-1]):
                if i == '1': 
                    C = C * D[c]
            return C
    
    def bitLength(self,number):
        return len(number.baseN(2))
    

    def divMod(self,other):
        if other.number == [0]:
            return None
        elif self == other:
            return bn(1)
        elif self < other:
            return bn(0), self
        else:
            B = bn(self.number)
            A = bn(other.number)
            c = 1 
            while A.base10() <= B.base10():
                A.lshift(1)
                c = c << 1
            c = c >> 1
            res = bn(0)
            A.rshift(1)
            c = bn(c)
            while not (c == bn(0)):
                if B.base10() >= A.base10():
                    B = B - A
                    res = res + c
                c.rshift(1)
                A.rshift(1)
            return res,B


    def __truediv__(self,other):
        return self.divMod(other)[0]


    def __mod__(self,other):
        return self.divMod(other)[1]


    def lshift(self,bits):
        lshiftBits(self,bits)
    

    def rshift(self, bits):
        rshiftBits(self,bits)


def karatsubaStep(a,b):
    #print(a.base10())
    if a.length == 1 or b.length == 1:
        result = bn(0)
        for c,b_d in enumerate(b.number):
            tmp = a.mulStep(b_d)
            tmp = shiftLeft(tmp,c)
            result = result + bn(tmp)
        return result
    else:
        n = max(a.length,b.length)
        #print(a.length,b.length,n)
        m = n // 2
        a = a.number 
        b = b.number
        a_l,a_h = bn(a[:m]),bn(a[m:])
        b_l,b_h = bn(b[:m]),bn(b[m:])
        z0 = karatsubaStep(a_h,b_h)
        z2 = karatsubaStep(a_l,b_l)
        z1 = karatsubaStep(a_l,b_h) + karatsubaStep(a_h,b_l)
        z1 = karatsubaStep(a_l+a_h,b_l+b_h) - z0 - z2
        z0_f = bn(shiftLeft(z0.number,n))
        z1_f = bn(shiftLeft(z1.number,m))

        z = z0_f + z1_f + z2
        return z 
def shiftLeft( number, t):
    return [0]*t + number

def shiftRight(number,t):
    return number[t:]

def lshiftBits(num,bits):
    word = num.Bp 
    b_words = bits // word 
    b_shift = bits % word
    if b_words != 0:
        num.number = [0]*b_words + num.number
        num.length += b_words
    if b_shift != 0:
        result = num.number + [0]
        num.length += 1
        for i in range(num.length-1,0,-1):
            curr = (result[i] << b_shift) & ((1 << (64)) - 1)
            result[i] = curr | (result[i-1] >> (word - b_shift))
        result[0] = (result[0] << b_shift) & ((1 << (word)) - 1)
        if set(result) == {0}: result = [0]
        num.number = result
        num.length = len(result)

def rshiftBits(num, bits):
    word = num.Bp
    b_words = bits // word
    b_shift = bits % word
    if b_words != 0:
        num.number = num.number[b_words:] + [0]*b_words
        if num.number == []: num.number = [0]
        # num.length -= b_words

    if b_shift != 0:
        result = num.number
        for i in range(num.length-1):
            prev = result[i+1] & ((1 << b_shift) - 1)
            result[i] = (result[i] >> b_shift) | (prev << (word - b_shift))
        result[-1] = result[-1] >> b_shift
        if set(result) == {0}: result = [0]
        num.number = result
        num.length = len(result)
    