HEX_DIGITS = "0123456789ABCDEF"

def getDigits(number:int,base:int) -> list:
    digits = [] 
    if number == 0:
        return [0]
    elif number == 1:
        return [1]
    while number > 0:
        remainder = number % base
        digits.append(remainder)
        number = number // base
    return digits

def convert(number,base):
    digits = []
    sign = 0  
    if isinstance(number,int):
        if number < 0: 
            number = number * -1
            sign = -1
        else:
            sign = 1
        digits = getDigits(number,base)
    elif isinstance(number,list):    
        for digit in number:
            if digit > base:
                raise TypeError('Wrong input: List have incorrect base.')
            else:
                # while number and number[-1] == 0:
                #     number.pop()
                digits = number
                sign = 1
    elif isinstance(number,str):
        try:
            number = int(number)
            if number < 0: 
                sign = -1
                number = -1 * number
            else: 
                sign = 1
            digits = getDigits(number,base)
        except: 
            if number[0] == "-":
                sign = -1
                number = number[1:]
            else: 
                sign = 1
            if "0x" in number:
                number = number[number.index("0x")+2:]
            s = set([item for item in number.upper() if item not in HEX_DIGITS])
            if len(s) > 0:
                raise TypeError("Wrong input: Unknown string format")
            else:
                number = int(number,16)
                digits = getDigits(number,base)

    return digits, sign

