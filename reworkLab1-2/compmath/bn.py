import ctypes
from . import bnTypes
BASE = 2
BASE_POWER = 64
nblib = ctypes.CDLL('/home/gratigo/Documents/term5/SROM/lab1/prikhodko_fb12_lab1/reworkLab1-2/compmath/bnMath.so')
def compare(a,b):
    a_D = list(a.digits)
    b_D = list(b.digits)    
    size = max(len(b_D),len(a_D))
    a_c = (ctypes.c_uint64 * size)(*a_D)
    b_c = (ctypes.c_uint64 * size)(*b_D)
    result_c = (ctypes.c_uint64 * size)() 
    borrow = 0
    borrow = nblib.bn_sub(result_c,a_c,b_c,size)
    return borrow != 0

class bn:
    def __init__(self,number,sign=0):
        self.bp = BASE_POWER
        self.base = BASE**BASE_POWER
        self.digits,t_s = bnTypes.convert(number,self.base)
        if sign == 0: self.sign = t_s
        else: self.sign = sign
        self.length = len(self.digits)

    def __add__(self,other):
        sign = 1
        if self.sign == -1:
            if other.sign == -1:
                sign = -1
            else:
                a = bn(self.digits)
                return other.__sub__(a)
        elif other.sign == -1:
            a = bn(other.digits)
            return self.__sub__(a)
        self_D = list(self.digits)
        other_D = list(other.digits)
        size = max(len(other_D),len(self_D)) + 1
        self_c = (ctypes.c_uint64 * size)(*self_D)
        other_c = (ctypes.c_uint64 * size)(*other_D)
        result_c = (ctypes.c_uint64 * size)() 
        nblib.bn_add(result_c,self_c,other_c,size)
        result = list(result_c)
        return bn(result,sign)

    

    def __sub__(self,other):
        if self.sign == -1:
            if other.sign == -1:
                a = bn(self.digits)
                b = bn(other.digits)
                return b.__sub__(a)
            else:
                a = bn(self.digits)
                res = a.__add__(other)
                res.sign = -1
                return res
        elif other.sign == -1:
            a = bn(other.digits)
            return self.__add__(a)
        self_D = list(self.digits)
        other_D = list(other.digits)    
        size = max(len(other_D),len(self_D))
        self_c = (ctypes.c_uint64 * size)(*self_D)
        other_c = (ctypes.c_uint64 * size)(*other_D)
        result_c = (ctypes.c_uint64 * size)() 
        borrow = 0
        borrow = nblib.bn_sub(result_c,self_c,other_c,size)
        if borrow != 0:
            nblib.bn_sub(result_c,other_c,self_c,size)
            return bn(list(result_c),-1)
        return bn(list(result_c))


    def __mul__(self,other):
        n = max(self.length,other.length)
        if n == 1: n = 0
        self_D = list(self.digits + [0]*(n-self.length))
        other_D = list(other.digits + [0]*(n-other.length))
        size = max(len(other_D),len(self_D))
        self_c = (ctypes.c_uint64 * size)(*self_D)
        other_c = (ctypes.c_uint64 * size)(*other_D)
        result_c = (ctypes.c_uint64 * (size*2))()
        nblib.bn_kMul(result_c,self_c,other_c,size)
        return bn(list(result_c))

    def lshB(self):
        self_D = list(self.digits+[0])
        size = len(self_D)
        self_c = (ctypes.c_uint64 * size)(*self_D)
        nblib.lshiftB(self_c,size)
        result = list(self_c)
        while len(result) > 1 and result[-1] == 0:
            result.pop()
        self.digits = result
    
    def rshB(self):
        self_D = list(self.digits+[0])
        size = len(self_D)
        self_c = (ctypes.c_uint64 * size)(*self_D)
        nblib.rshiftB(self_c,size)
        result = list(self_c)
        while len(result) > 1 and result[-1] == 0:
            result.pop()
        self.digits = result
        
    
    def __truediv__(self,other):
        if other.digits == [0]:
            return None
        elif self == other:
            return bn(1)
        elif self < other:
            return bn(0)
        elif other == bn(1):
            return self
        else:
            self_D = list(self.digits)
            other_D = list(other.digits)    
            size = max(len(other_D),len(self_D))+1
            self_c = (ctypes.c_uint64 * size)(*self_D)
            other_c = (ctypes.c_uint64 * size)(*other_D)
            result_c = (ctypes.c_uint64 * size)()
            reminder_c = (ctypes.c_uint64 * size)()
            nblib.bn_div(result_c, reminder_c, self_c, other_c, size)
            result = list(result_c) 
            while len(result) > 1 and result[-1] == 0:
                result.pop()
            return bn(result)

    def __mod__(self,other):
        if other.digits == [0]:
            return None
        elif self == other:
            return bn(0)
        elif self < other:
            return self
        elif other == bn(1):
            return bn(0)
        else:
            self_D = list(self.digits)
            other_D = list(other.digits)    
            size = max(len(other_D),len(self_D))+1
            self_c = (ctypes.c_uint64 * size)(*self_D)
            other_c = (ctypes.c_uint64 * size)(*other_D)
            result_c = (ctypes.c_uint64 * size)()
            reminder_c = (ctypes.c_uint64 * size)()
            nblib.bn_div(result_c, reminder_c, self_c, other_c, size)
            reminder = list(reminder_c) 
            while len(reminder) > 1 and reminder[-1] == 0:
                reminder.pop()
            return bn(reminder)

    def __ge__(self,other):
        print(self.length,other.length)
        if self.length == other.length:
            return not compare(self,other)
        else:
            return self.length == max(self.length,other.length)

    def __le__(self,other):
        # self_D = list(self.digits)
        # other_D = list(other.digits)    
        # size = max(len(other_D),len(self_D))
        # self_c = (ctypes.c_uint64 * size)(*self_D)
        # other_c = (ctypes.c_uint64 * size)(*other_D)
        # res = nblib.bn_le(self_c,other_c,size)
        # return res == 1
        if self.length == other.length:
            return not compare(other,self)
        else:
            return self.length == min(self.length,other.length)

    def __gt__(self,other):
        if self.__eq__(other): return False
        else: return self.__ge__(other)

    def __lt__(self,other):
        if self.__eq__(other): return False
        else: return self.__le__(other)

    def __eq__(self,other):
        s_n = list(self.digits) 
        o_n = list(other.digits)
        while s_n[-1] == 0 and len(s_n) > 1:
            s_n.pop()
        while o_n[-1] == 0 and len(o_n) > 1:
            o_n.pop()
        if s_n == o_n:
            return True
        else: 
            return False

    def __str__(self):
        return ", ".join([str(item) for item in self.digits])
    
    def __repr__(self):
        """for ipython3"""
        return ",".join([str(item) for item in self.digits])

    def base10(self) -> int:
        res = 0
        for digit in self.digits[::-1]:
            res = res * self.base + digit
        return res * self.sign
    
    def baseN(self,baseN:int):
        if baseN not in [2,10,16]:
            raise TypeError("Invalid convertion base or not implemented yet")
        if baseN == 10:
            return self.base10()
        res = ""
        
        for item in self.digits:
                
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



