import ctypes
from . import bnTypes

BASE = 2
BASE_POWER = 64
nblib = ctypes.CDLL('compmath/bnMath.so')


def compare(a,b):
    a_D = list(a.digits)
    b_D = list(b.digits)    
    # size = max(len(b_D),len(a_D))
    # a_c = (ctypes.c_uint64 * size)(*a_D)
    # b_c = (ctypes.c_uint64 * size)(*b_D)
    # result_c = (ctypes.c_uint64 * size)() 
    # borrow = 0
    # borrow = nblib.bn_sub(result_c,a_c,b_c,size)
    for i in range(a.length-1,-1,-1):
        if a_D[i] > b_D[i]:
            return True
        elif a_D[i] < b_D[i]:
            return False
    return True

def conv(number,baset):
    result = []
    for i in number:
        tmp = bnTypes.getDigits(i,baset)[::-1]
        result = [0]*(BASE_POWER-len(tmp))+tmp+result
    return result

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
            result_c = list(result_c)
            while len(result_c) > 1 and result_c[-1] == 0:
                result_c.pop()
            return bn(result_c,-1)
        result_c = list(result_c)
        while len(result_c) > 1 and result_c[-1] == 0:
                result_c.pop()
        return bn(result_c)


    def __mul__(self,other):
        n = max(self.length,other.length)
        sign = self.sign * other.sign
        if n == 1: n = 0
        self_D = list(self.digits + [0]*(n-self.length))
        other_D = list(other.digits + [0]*(n-other.length))
        size = max(len(other_D),len(self_D))
        self_c = (ctypes.c_uint64 * size)(*self_D)
        other_c = (ctypes.c_uint64 * size)(*other_D)
        result_c = (ctypes.c_uint64 * (size*2))()
        nblib.bn_kMul(result_c,self_c,other_c,size)
        return bn(list(result_c),sign)

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

    
    def __pow__(self,power):
        if power == bn(0):
            return bn(1)
        elif power == bn(1):
            return self
        elif power == bn(2):
            return self.__mul__(self)
        else:
            t = 2
            self_D = list(self.digits)
            other_D = conv(list(power.digits),2)[::-1]
            rsize = len(self_D) * (2**len(other_D)) 
            self_c = (ctypes.c_uint64 * (rsize))(*self_D)
            other_c = (ctypes.c_uint64 * len(other_D))(*other_D)
            result_c = (ctypes.c_uint64 * rsize)()
            nblib.bn_pow(result_c,self_c,other_c,len(self_D ),len(other_D))
            return bn(list(result_c))

    def __ge__(self,other):
        #print(self.length,other.length)
        if self.__eq__(other): return True
        if self.length == other.length:
            # print("we are in same length compare is called")
            return  compare(self,other)
        else:
            # print("length is different - higher wins")
            return self.length == max(self.length,other.length)

    def __le__(self,other):
        # self_D = list(self.digits)
        # other_D = list(other.digits)    
        # size = max(len(other_D),len(self_D))
        # self_c = (ctypes.c_uint64 * size)(*self_D)
        # other_c = (ctypes.c_uint64 * size)(*other_D)
        # res = nblib.bn_le(self_c,other_c,size)
        # return res == 1
        if self.__eq__(other): return True
        if self.length == other.length:
            return not compare(self,other)
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
                res_t = bnTypes.HEX_DIGITS[remainder] + res_t
                item = item // baseN
            from math import log
            mod = (self.bp // int(log(baseN,BASE)))
            rem = mod - len(res_t) 
            res_t = "0"*rem + res_t
            res = res_t + res
        res = res.lstrip('0')
        if res == '': res = '0'
        return res if self.sign == 1 else "-" + res
    
    def evenC(self):
        if self.digits[0] % 2 == 0:
            return True
        return False

def gcd(a,b):
    if a > b:
        a_D = list(a.digits)
        b_D = list(b.digits)
        size = max(len(a_D),len(b_D))+1
        a_c = (ctypes.c_uint64 * size)(*a_D)
        b_c = (ctypes.c_uint64 * size)(*b_D)
        result_c = (ctypes.c_uint64 * size)()
        nblib.bn_gcd(result_c, a_c, b_c, size)
        return bn(list(result_c))
    else:
        return gcd(b,a)


def lcm(a,b):
    return a*b / gcd(a,b)



# def xgcd(a,b):
#     if a > b:
#         a_D = list(a.digits)
#         b_D = list(b.digits)
#         size = max(len(a_D),len(b_D))+1
#         a_c = (ctypes.c_uint64 * size)(*a_D)
#         b_c = (ctypes.c_uint64 * size)(*b_D)
#         result_c = (ctypes.c_uint64 * size)()
#         x = (ctypes.c_uint64 * size)()
#         y = (ctypes.c_uint64 * size)()
#         nblib.bn_gcd(result_c, a_c, b_c, size,x,y)
#         return bn(list(result_c)),bn(x),bn(y)
#     else:
#         return xgcd(b,a)
    


class Ring:
    """Ring class for working in finite field, integers mod nonprime N"""
    def __init__(self,mod):
        global MOD,MU,K,R
        MOD = bn(mod)
        self.mod = mod
        K = MOD.length
        MU = bn((BASE**BASE_POWER)**(2*K))/MOD
        R = bn(BASE**(BASE_POWER*K))
        # print("choose k:", (BASE**BASE_POWER)**K > mod )
        # print("My MU",MU.base10())
        # print("Calc MU",((BASE**BASE_POWER)**(2*K))//mod)
    def __call__(self,number):
        return RingElement(number)

class RingElement(bn):
    """Class for elements of Ring"""
    def __init__(self,number):
        res = number%MOD
        super().__init__(res.digits,number.sign)

    def __add__(self,other):
        result = super().__add__(RingElement(other))
        if result.sign == -1:
            result += MOD
            result.sign = 1
        return RingElement(result)
    
    def __sub__(self,other):
        result = super().__sub__(RingElement(other))
        if result.sign == -1:
            result += MOD
            result.sign = 1
        return RingElement(result)

    def __mul__(self,other):
        result = super().__mul__(RingElement(other))
        result = RingElement(result)
        if result.sign == -1:
            result += MOD
            result.sign = 1
        return result
    
    def __pow__(self,other):
        # print(self,other)
        if other == bn(0):
            return bn(1)
        elif other == bn(1):
            return self
        elif other == bn(2):
            return self.__mul__(self)
        else:
            # print("here")
            A = bn(self.digits)
            other_D = list(other.digits)
            other_b = conv(other_D,2)[::-1]
            # print(other_b)
            while len(other_b)>1 and other_b[-1] == 0:
                other_b.pop()
            # print(other_b)
            result = bn(1)
            for i in other_b:
                if i == 1:
                    # print(i)
                    # print(result,A,MOD)
                    result = barrettReduction(result*A)#(result*A)%MOD#barrettReduction(result*A)
                    # print("result adter b",result)
                # print("A",A)
                A = barrettReduction(A*A)#(A*A)%MOD#barrettReduction(A*A)
                # print("A after barret",A)
            # print(result)
            return RingElement(result)
            

def barrettReduction(a,mod=None):
    if isinstance(mod,type(None)): mod = MOD
    # if mod < bn(a.base):
    #     return a%mod
    number = bn(list(a.digits))
    number = number * MU
    for _ in range(2*K):
        number.length -= 1
        number.digits.pop(0)
    # for _ in range(K+1):
    #     number.length -= 1
    #     number.digits.pop(0)
    r = a - number * mod
    # print("r:",r,"mod:",mod)
    # print(r.base10() > mod.base10())
    # print(r.base10(),mod.base10())
    # print(r > mod)
    # print(r-mod-mod > mod)
    while r >= mod:
        #print(r, mod)
        # print("stuck here")
        r -= mod
    return r
