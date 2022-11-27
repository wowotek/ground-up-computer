from __future__ import annotations
import utils as UTILS


ARCH_BIT_BANDWITH = 266
BANDWITH_MAX_NUMBER = int("".join(["1" for _ in range(ARCH_BIT_BANDWITH)]), 2)

class Binary:
    def __init__(self, unsigned_decimal: int = 0):
        self.__val = unsigned_decimal
        if self.__val < 0:
            self.__val = BANDWITH_MAX_NUMBER - self.__val
        
        if self.__val > BANDWITH_MAX_NUMBER:
            self.__val = self.__val - BANDWITH_MAX_NUMBER

    @staticmethod
    def from_decimal(decimal: int):
        return Binary(decimal)
    
    @staticmethod
    def from_hex(hex: str):
        h = int(hex, 16)
        return Binary(h)
    
    @staticmethod
    def from_binary(binary: str):
        binary = binary.replace("0b", "").rjust(ARCH_BIT_BANDWITH, "0")
        
        return Binary(int(binary, 2))
    
    @staticmethod
    def maximum():
        return Binary.from_decimal(BANDWITH_MAX_NUMBER)
    
    @property
    def binary(self):
        return bin(self.__val).replace("0b", "").rjust(ARCH_BIT_BANDWITH, "0") 
    
    @property
    def hex(self):
        return hex(self.__val).replace("0x", "")

    @property
    def signed_decimal(self):
        return self.__val - BANDWITH_MAX_NUMBER

    @property
    def unsigned_decimal(self):
        return self.__val
    
    def set_unsigned_decimal(self, unsigned_decimal: int):
        self.__val = unsigned_decimal
        if self.__val < 0:
            self.__val = BANDWITH_MAX_NUMBER - self.__val
        
        if self.__val > BANDWITH_MAX_NUMBER:
            self.__val = self.__val - BANDWITH_MAX_NUMBER

    @property
    def SUM_OR(self):
        init = True if self.binary[0] == "1" else False
        for i in self.binary[1::]:
            init = init or (True if i == "1" else False)

        return init

    @property
    def SUM_AND(self):
        init = True if self.binary[0] == "1" else False
        for i in self.binary[1::]:
            init = init and (True if i == "1" else False)

        return init

    @property
    def copy(self):
        return Binary.from_decimal(self.unsigned_decimal)

    def OR(self, other: Binary):
        return Binary.from_decimal(self.unsigned_decimal | other.unsigned_decimal)
    
    def NOR(self, other: Binary):
        return Binary.from_decimal(~(self.unsigned_decimal | other.unsigned_decimal))
        
    def AND(self, other: Binary):
        return Binary.from_decimal(self.unsigned_decimal & other.unsigned_decimal)
        
    def NAND(self, other: Binary):
        return Binary.from_decimal(~(self.unsigned_decimal & other.unsigned_decimal))
        
    def XOR(self, other: Binary):
        return Binary.from_decimal(self.unsigned_decimal ^ other.unsigned_decimal)
    
    def XNOR(self, other: Binary):
        return Binary.from_decimal(~(self.unsigned_decimal ^ other.unsigned_decimal))

    @staticmethod
    def adder_subtractor(value_a: Binary, value_b: Binary, carry: bool = False, subtract: bool = False):
        t_binary = [True if i == "1" else False for i in value_a.binary][::-1]
        o_binary = [True if i == "1" else False for i in (value_b.binary if not subtract else value_b.XOR(Binary.maximum())).binary][::-1]

        results: list[bool] = []
        last_carry = carry or subtract
        for i in range(ARCH_BIT_BANDWITH):
            r, c = UTILS.full_adder(t_binary[i], o_binary[i], last_carry)
            results.append(r)
            last_carry = c

        parsed_result = "".join(["1" if i else "0" for i in results][::-1])

        is_negative = False
        if subtract:
            is_negative = (value_a.unsigned_decimal - value_b.unsigned_decimal) < 0

        return Binary.from_binary(parsed_result), bool(last_carry), is_negative
    
    def ADD(self, other: Binary, carry: bool = False):
        return Binary.adder_subtractor(self.copy, other.copy, carry, False)
    
    def SUBTRACT(self, other: Binary):
        return Binary.adder_subtractor(self.copy, other.copy, subtract=True)

    def MULTIPLY(self, other: Binary):
        last_result = Binary.from_decimal(0)
        last_carry = False
        for _ in range(other.unsigned_decimal):
            last_result, last_carry, is_negative = last_result.ADD(self.copy, last_carry)

        return last_result, last_carry, is_negative
    
    def DIVIDE(self, other: Binary):
        a = self.binary
        b = other.binary

        result = ''
        temp = '0'
        r = 0

        for i in range(len(a)):        
            if int(b) > int(temp):
                result += '0'
                temp += a[i]
            else:
                r = Binary.from_binary(temp).SUBTRACT(Binary.from_binary(b))[0].unsigned_decimal
                if r == 0:
                    temp = a[i]
                    result += '1'
                else:
                    r = str(r).lstrip('0')
                    result += '1'
                    temp = r + a[i]
        
        if temp != int(0): 
            result = result + '0' 
                    
        return Binary.from_binary(result)


    def __str__(self):
        binaries = UTILS.split_every_nth(self.binary, 8)
        hexes = " ".join([hex(int(i, 2)).replace("0x", "").rjust(2, "0") for i in binaries if int(i, 2) != 0])
        decimal = f"{self.unsigned_decimal:,}"
        sdecimal = f"{self.signed_decimal:,}"

        return f"{hexes} | {decimal} | {sdecimal}"

    def __repr__(self):
        return self.__str__()


__INSTRUCTION_BANDWITH = 10
__PROC_CURRENT_INSTRUCTION = Binary(0)
__PROC_CURRENT_VALUE_A = Binary(0)
__PROC_CURRENT_VALUE_B = Binary(0)

RAM: dict[int, Binary] = {}
def initialize_ram(data: list[Binary]):
    for i in range(len(data)):
        RAM[i] = data[i]

REGISTRY = {
    0   : Binary(),   # Instruction Pointer - Program Counter
    1   : Binary(),   # Instruction
    2   : Binary(),   # ALU Return
    # ALUs
    # 0 Overflow
    # 1 Zero
    # 2 Negative
    # 3 Carry

    3   : Binary(),   # Flags Register

    4   : Binary(),   # General Purpose Register A
    5   : Binary(),   # General Purpose Register B
    6   : Binary(),   # General Purpose Register C
    7   : Binary(),   # General Purpose Register D
    8   : Binary(),   # General Purpose Register E
    9   : Binary(),   # General Purpose Register F
    10  : Binary(),   # General Purpose Register G
    11  : Binary(),   # General Purpose Register H

    12  : Binary(),   # General Purpose Unsigned Integer Register A
    13  : Binary(),   # General Purpose Unsigned Integer Register B

    14  : Binary(),   # General Purpose Signed Integer Register A
    15  : Binary(),   # General Purpose Signed Integer Register B

    16  : Binary(),   # General Purpose Unsigned Float Register A
    17  : Binary(),   # General Purpose Unsigned Float Register B

    18  : Binary(),   # General Purpose Signed Float Register A
    19  : Binary(),   # General Purpose Signed Float Register B
}

REGISTRY_NAMES = {
    "RFP": 0,
    "RFI": 1,
    "RFR": 2,

    "RFF": 3,

    "RGA": 4,
    "RGB": 5,
    "RGC": 6,
    "RGD": 7,
    "RGE": 8,
    "RGF": 9,
    "RGG": 10,
    "RGH": 11,

    "RIA": 12,
    "RIB": 13,
    "RIC": 14,
    "RID": 15,

    "RFA": 16,
    "RFB": 17,
    "RFC": 18,
    "RFD": 19
}

def _OP_NOP():
    for i in range(100000000):
        pass

def _OP_HALT():
    global IS_HALTING

    IS_HALTING = True

def _OP_OR():
    result = __PROC_CURRENT_VALUE_A.OR(__PROC_CURRENT_VALUE_B)
    REGISTRY[2] = result

def _OP_NOR():
    result = __PROC_CURRENT_VALUE_A.NOR(__PROC_CURRENT_VALUE_B)
    REGISTRY[2] = result

def _OP_AND():
    result = __PROC_CURRENT_VALUE_A.AND(__PROC_CURRENT_VALUE_B)
    REGISTRY[2] = result

def _OP_NAND():
    result = __PROC_CURRENT_VALUE_A.NAND(__PROC_CURRENT_VALUE_B)
    REGISTRY[2] = result

def _OP_XOR():
    result = __PROC_CURRENT_VALUE_A.XOR(__PROC_CURRENT_VALUE_B)
    REGISTRY[2] = result

def _OP_XNOR():
    result = __PROC_CURRENT_VALUE_A.XNOR(__PROC_CURRENT_VALUE_B)
    REGISTRY[2] = result

def _OP_ADD():
    result = __PROC_CURRENT_VALUE_A.ADD(__PROC_CURRENT_VALUE_B)
    REGISTRY[2] = result[0]

def _OP_SUB():
    result = __PROC_CURRENT_VALUE_A.SUBTRACT(__PROC_CURRENT_VALUE_B)
    REGISTRY[2] = result[0]

def _OP_MUL():
    result = __PROC_CURRENT_VALUE_A.MULTIPLY(__PROC_CURRENT_VALUE_B)
    REGISTRY[2] = result[0]

def _OP_DIV():
    result = __PROC_CURRENT_VALUE_A.DIVIDE(__PROC_CURRENT_VALUE_B)
    REGISTRY[2] = result[0]

def _OP_CMP():
    pass

def _OP_MOV():
    pass

def _OP_MEMSET():
    pass

def _OP_SET():
    pass

def _OP_LOAD():
    pass

def _OP_STORE():
    pass

def _OP_LEA():
    pass

def _OP_JUMP():
    pass

def _OP_JMZ():
    pass

def _OP_JMN():
    pass

def _OP_JEQ():
    pass

def _OP_JNE():
    pass

def _OP_JMG():
    pass

def _OP_JML():
    pass

OPERATIONS = {
    0: _OP_NOP,
    1: _OP_HALT,

    2: _OP_MOV,      # Copy from reg of src to reg dest
    3: _OP_SET,      # Set registry src to constant
    4: _OP_MEMSET,   # Set ram address to a constant
    5: _OP_LOAD,     # Load from ram address of src to reg of dest
    6: _OP_STORE,    # Store from reg of src to ram at dest
    7: _OP_LEA,      # Load Effective Address (load the address instead of value)

    # Conditional Jumps
    100: _OP_JUMP,     # do Unconditional Jump
    101: _OP_JMZ,      # Read From Flags and do Jump if flag is Zero
    102: _OP_JMN,      # Read From Flags and do Jump if flag is Negative
    103: _OP_JEQ,      # Read From Flags and do Jump if flag is Equal
    104: _OP_JNE,      # Read From Flags and do Jump if flag is Not Equal
    105: _OP_JMG,      # Read From Flags and do Jump if flag is Greater Than
    106: _OP_JML,      # Read From Flags and do Jump if flag is Less Than,

    200: _OP_OR,
    201: _OP_NOR,
    202: _OP_AND,
    203: _OP_NAND,
    204: _OP_XOR,
    205: _OP_XNOR,

    301: _OP_ADD,
    302: _OP_SUB,
    303: _OP_MUL,
    304: _OP_DIV,
    305: _OP_CMP,
}


###### FLAGS
# 0 = Carry
# 1 = Zero
# 2 = Negative
# 3 = Overflow
#
#
#
from random import randint

def tick():
    if IS_HALTING: return
    global __PROC_CURRENT_INSTRUCTION
    global __PROC_CURRENT_VALUE_A
    global __PROC_CURRENT_VALUE_B

    # Fetch
    REGISTRY[1] = RAM[REGISTRY[0].unsigned_decimal].copy

    # Decode
    __instruction = REGISTRY[1].binary[:__INSTRUCTION_BANDWITH:]
    __value_a = REGISTRY[1].binary[__INSTRUCTION_BANDWITH:((ARCH_BIT_BANDWITH - __INSTRUCTION_BANDWITH) // 2) + __INSTRUCTION_BANDWITH:]
    __value_b = REGISTRY[1].binary[((ARCH_BIT_BANDWITH - __INSTRUCTION_BANDWITH) // 2) + __INSTRUCTION_BANDWITH:ARCH_BIT_BANDWITH:]

    __PROC_CURRENT_INSTRUCTION = Binary.from_binary(__instruction)
    __PROC_CURRENT_VALUE_A = Binary.from_binary(__value_a)
    __PROC_CURRENT_VALUE_B = Binary.from_binary(__value_b)
    
    try:
        operation = OPERATIONS[__PROC_CURRENT_INSTRUCTION]
    except:
        print("Operation Not Found!")
        global IS_HALTING
        IS_HALTING = True
    
    operation()
    REGISTRY[0] = REGISTRY[0].set_unsigned_decimal(REGISTRY[0].unsigned_decimal + 1)


initialize_ram([
    Binary.from_decimal(randint(0, BANDWITH_MAX_NUMBER))
])

tick()