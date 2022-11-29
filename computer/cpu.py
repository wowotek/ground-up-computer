from __future__ import annotations
import utils as UTILS
import random

DEBUG = True
def eprint(*args, **kwargs):
    if not DEBUG: return
    print(*args, **kwargs)

ARCH_BIT_BANDWITH = 256
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
        o_binary = [True if i == "1" else False for i in (value_b.binary if not subtract else value_b.XOR(Binary.maximum()).binary)][::-1]

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

    def SHIFT_LEFT(self):
        binary = [i for i in self.binary]
        binary.append(binary.pop(0))
        return Binary.from_binary(binary)
    
    def SHIFT_RIGHT(self):
        binary = [i for i in self.binary]
        binary.insert(0, binary.pop())
        return Binary.from_binary(binary)

    def __str__(self):
        binaries = UTILS.split_every_nth(self.binary, 8)
        hexes = " ".join([hex(int(i, 2)).replace("0x", "").rjust(2, "0") for i in binaries if int(i, 2) != 0])
        decimal = f"{self.unsigned_decimal:,}"
        sdecimal = f"{self.signed_decimal:,}"

        return f"{hexes}"

    def __repr__(self):
        return self.__str__()


__INSTRUCTION_BANDWITH = 10
__PROC_CURRENT_INSTRUCTION = Binary(0)
__PROC_CURRENT_VALUE_A = Binary(0)
__PROC_CURRENT_VALUE_B = Binary(0)
__IS_HALTING = False

PROGRAM_LENGTH = 0
RAM: dict[int, Binary] = {}
def initialize_ram(data: list[Binary]):
    global PROGRAM_LENGTH
    for i in range(len(data)):
        RAM[i] = data[i]
    
    PROGRAM_LENGTH = len(data) - (320 * 320)
    if PROGRAM_LENGTH < 0:
        PROGRAM_LENGTH = len(data)


REGISTRY = {
    0   : Binary(),   # Instruction Pointer - Program Counter
    1   : Binary(),   # Instruction
    2   : Binary(),   # ALU Return

    3   : Binary(),   # Flags Register
    # 0 -1 Overflow
    # 1 -2 Zero
    # 2 -3 Negative
    # 3 -4 Carry
    # 4 -5 Underflow

    4   : Binary(),   # General Purpose Register A
    5   : Binary(),   # General Purpose Register B
    6   : Binary(),   # General Purpose Register C
    7   : Binary(),   # General Purpose Register D
    8   : Binary(),   # General Purpose Register E
    9   : Binary(),   # General Purpose Register F
    10  : Binary(),   # General Purpose Register G
    11  : Binary(),   # General Purpose Register H
}

REGISTRY_NAMES = {
    0   : "RFP",
    1   : "RFI",
    2   : "RFR",
    3   : "RFF",
    4   : "RGA",
    5   : "RGB",
    6   : "RGC",
    7   : "RGD",
    8   : "RGE",
    9   : "RGF",
    10  : "RGG",
    11  : "RGH",
}

def assign_flag(overflow: bool = False, zero: bool = False, negative: bool = False, carry: bool = False, underflow: bool = False):
    current = [i for i in Binary.from_decimal(0).binary]
    if overflow:
        current[-1] = "1"
    if zero:
        current[-2] = "1"
    if negative:
        current[-3] = "1"
    if carry:
        current[-4] = "1"
    if underflow:
        current[-5] = "1"

def _OP_NOP():
    for i in range(100000000):
        pass

def _OP_HALT():
    global __IS_HALTING

    __IS_HALTING = True

def _OP_MOV():
    eprint("MOV", REGISTRY_NAMES[__PROC_CURRENT_VALUE_A.unsigned_decimal], REGISTRY_NAMES[__PROC_CURRENT_VALUE_B.unsigned_decimal])
    REGISTRY[__PROC_CURRENT_VALUE_B.unsigned_decimal] = REGISTRY[__PROC_CURRENT_VALUE_A.unsigned_decimal].copy

def _OP_MEMSET():
    eprint("MEM", __PROC_CURRENT_VALUE_A.unsigned_decimal, __PROC_CURRENT_VALUE_B.unsigned_decimal)
    RAM[__PROC_CURRENT_VALUE_A.unsigned_decimal] = Binary.from_decimal(__PROC_CURRENT_VALUE_B.unsigned_decimal)

def _OP_SET():
    eprint("SET", __PROC_CURRENT_VALUE_A.unsigned_decimal, __PROC_CURRENT_VALUE_B.unsigned_decimal)
    REGISTRY[__PROC_CURRENT_VALUE_A.unsigned_decimal] = __PROC_CURRENT_VALUE_B.copy

def _OP_LOAD():
    eprint("LOA", __PROC_CURRENT_VALUE_A.unsigned_decimal, __PROC_CURRENT_VALUE_B.unsigned_decimal)
    REGISTRY[__PROC_CURRENT_VALUE_A.unsigned_decimal] = RAM[__PROC_CURRENT_VALUE_B.unsigned_decimal].copy

def _OP_STORE():
    eprint("STO", __PROC_CURRENT_VALUE_A.unsigned_decimal, __PROC_CURRENT_VALUE_B.unsigned_decimal)
    RAM[__PROC_CURRENT_VALUE_B.unsigned_decimal] = REGISTRY[__PROC_CURRENT_VALUE_A.unsigned_decimal].copy
    print()

def _OP_LEA():
    eprint("LEA", __PROC_CURRENT_VALUE_A.unsigned_decimal, __PROC_CURRENT_VALUE_B.unsigned_decimal)

def _OP_RND(): # Randomize until maximum
    global RAM
    eprint("RND", __PROC_CURRENT_VALUE_A.unsigned_decimal, __PROC_CURRENT_VALUE_B.unsigned_decimal)
    REGISTRY[__PROC_CURRENT_VALUE_A.unsigned_decimal] = Binary.from_decimal(random.randint(0, BANDWITH_MAX_NUMBER))

def _OP_RNDC(): # Randomize with Ceiling
    eprint("RNDC", __PROC_CURRENT_VALUE_A.unsigned_decimal, __PROC_CURRENT_VALUE_B.unsigned_decimal)
    REGISTRY[__PROC_CURRENT_VALUE_A.unsigned_decimal] = Binary.from_decimal(random.randint(0, __PROC_CURRENT_VALUE_B.unsigned_decimal))

def _OP_RNDS(): # Randomize Signed
    eprint("RNDS", __PROC_CURRENT_VALUE_A.unsigned_decimal, __PROC_CURRENT_VALUE_B.unsigned_decimal)
    REGISTRY[__PROC_CURRENT_VALUE_A.unsigned_decimal] = Binary.from_decimal(random.randint(-(BANDWITH_MAX_NUMBER/2), BANDWITH_MAX_NUMBER/2))

def _OP_STORER():
    eprint("STORER", __PROC_CURRENT_VALUE_A.unsigned_decimal, __PROC_CURRENT_VALUE_B.unsigned_decimal)
    RAM[REGISTRY[__PROC_CURRENT_VALUE_B.unsigned_decimal].unsigned_decimal] = REGISTRY[__PROC_CURRENT_VALUE_A.unsigned_decimal].copy

def _OP_JMP():
    eprint("JMP", __PROC_CURRENT_VALUE_A.unsigned_decimal, __PROC_CURRENT_VALUE_B.unsigned_decimal)
    REGISTRY[0] = Binary.from_decimal(__PROC_CURRENT_VALUE_A.unsigned_decimal)

def _OP_JEZ():
    eprint("JEZ", __PROC_CURRENT_VALUE_A.unsigned_decimal, __PROC_CURRENT_VALUE_B.unsigned_decimal)
    if REGISTRY[3].binary[-2] == "1" and REGISTRY[3].binary[-3] == "0":
        REGISTRY[0] = Binary.from_decimal(__PROC_CURRENT_VALUE_A.unsigned_decimal)

def _OP_JEQ():
    eprint("JEQ", __PROC_CURRENT_VALUE_A.unsigned_decimal, __PROC_CURRENT_VALUE_B.unsigned_decimal)
    if REGISTRY[3].binary[-2] == "1" and REGISTRY[3].binary[-3] == "0":
        REGISTRY[0] = Binary.from_decimal(__PROC_CURRENT_VALUE_A.unsigned_decimal)

def _OP_JNE():
    eprint("JNE", __PROC_CURRENT_VALUE_A.unsigned_decimal, __PROC_CURRENT_VALUE_B.unsigned_decimal)
    if REGISTRY[3].binary[-2] == "0" or REGISTRY[3].binary[-3] == "1":
        REGISTRY[0] = Binary.from_decimal(__PROC_CURRENT_VALUE_A.unsigned_decimal)

def _OP_JMG():
    eprint("JMG", __PROC_CURRENT_VALUE_A.unsigned_decimal, __PROC_CURRENT_VALUE_B.unsigned_decimal)
    if REGISTRY[3].binary[-2] == "0" and REGISTRY[3].binary[-3] == "0":
        REGISTRY[0] = Binary.from_decimal(__PROC_CURRENT_VALUE_A.unsigned_decimal)

def _OP_JML():
    eprint("JML", __PROC_CURRENT_VALUE_A.unsigned_decimal, __PROC_CURRENT_VALUE_B.unsigned_decimal)
    if REGISTRY[3].binary[-2] == "0" and REGISTRY[3].binary[-3] == "1":
        REGISTRY[0] = Binary.from_decimal(__PROC_CURRENT_VALUE_A.unsigned_decimal)

def _OP_OR():
    eprint("OR", __PROC_CURRENT_VALUE_A.unsigned_decimal, __PROC_CURRENT_VALUE_B.unsigned_decimal)
    result = REGISTRY[__PROC_CURRENT_VALUE_A.unsigned_decimal].copy.OR(REGISTRY[__PROC_CURRENT_VALUE_B.unsigned_decimal])
    assign_flag(False, result.unsigned_decimal == 0, False, False)
    REGISTRY[2] = result

def _OP_NOR():
    eprint("NOR", __PROC_CURRENT_VALUE_A.unsigned_decimal, __PROC_CURRENT_VALUE_B.unsigned_decimal)
    result = REGISTRY[__PROC_CURRENT_VALUE_A.unsigned_decimal].copy.NOR(REGISTRY[__PROC_CURRENT_VALUE_B.unsigned_decimal])
    assign_flag(False, result.unsigned_decimal == 0, False, False)
    REGISTRY[2] = result

def _OP_AND():
    eprint("AND", __PROC_CURRENT_VALUE_A.unsigned_decimal, __PROC_CURRENT_VALUE_B.unsigned_decimal)
    result = REGISTRY[__PROC_CURRENT_VALUE_A.unsigned_decimal].copy.AND(REGISTRY[__PROC_CURRENT_VALUE_B.unsigned_decimal])
    assign_flag(False, result.unsigned_decimal == 0, False, False)
    REGISTRY[2] = result

def _OP_NAND():
    eprint("NAN", __PROC_CURRENT_VALUE_A.unsigned_decimal, __PROC_CURRENT_VALUE_B.unsigned_decimal)
    result = REGISTRY[__PROC_CURRENT_VALUE_A.unsigned_decimal].copy.NAND(REGISTRY[__PROC_CURRENT_VALUE_B.unsigned_decimal])
    assign_flag(False, result.unsigned_decimal == 0, False, False)
    REGISTRY[2] = result

def _OP_XOR():
    eprint("XOR", __PROC_CURRENT_VALUE_A.unsigned_decimal, __PROC_CURRENT_VALUE_B.unsigned_decimal)
    result = REGISTRY[__PROC_CURRENT_VALUE_A.unsigned_decimal].copy.XOR(REGISTRY[__PROC_CURRENT_VALUE_B.unsigned_decimal])
    assign_flag(False, result.unsigned_decimal == 0, False, False)
    REGISTRY[2] = result

def _OP_XNOR():
    eprint("XNO", __PROC_CURRENT_VALUE_A.unsigned_decimal, __PROC_CURRENT_VALUE_B.unsigned_decimal)
    result = REGISTRY[__PROC_CURRENT_VALUE_A.unsigned_decimal].copy.XNOR(REGISTRY[__PROC_CURRENT_VALUE_B.unsigned_decimal])
    assign_flag(False, result.unsigned_decimal == 0, False, False)
    REGISTRY[2] = result

def _OP_INC():
    eprint("INC", __PROC_CURRENT_VALUE_A.unsigned_decimal, __PROC_CURRENT_VALUE_B.unsigned_decimal)
    REGISTRY[__PROC_CURRENT_VALUE_A.unsigned_decimal] = Binary.from_decimal(REGISTRY[__PROC_CURRENT_VALUE_A.unsigned_decimal].unsigned_decimal + 1)

def _OP_DEC():
    eprint("DEC", __PROC_CURRENT_VALUE_A.unsigned_decimal, __PROC_CURRENT_VALUE_B.unsigned_decimal)
    REGISTRY[__PROC_CURRENT_VALUE_A.unsigned_decimal] = Binary.from_decimal(REGISTRY[__PROC_CURRENT_VALUE_A.unsigned_decimal].unsigned_decimal - 1)

def _OP_ADD():
    eprint("ADD", __PROC_CURRENT_VALUE_A.unsigned_decimal, __PROC_CURRENT_VALUE_B.unsigned_decimal, (REGISTRY[__PROC_CURRENT_VALUE_A.unsigned_decimal].unsigned_decimal, REGISTRY[__PROC_CURRENT_VALUE_B.unsigned_decimal].unsigned_decimal))
    result = REGISTRY[__PROC_CURRENT_VALUE_A.unsigned_decimal].copy.ADD(REGISTRY[__PROC_CURRENT_VALUE_B.unsigned_decimal].copy)
    assign_flag((__PROC_CURRENT_VALUE_A.unsigned_decimal + __PROC_CURRENT_VALUE_B.unsigned_decimal) > BANDWITH_MAX_NUMBER, result[0].unsigned_decimal == 0, result[2], result[1], (__PROC_CURRENT_VALUE_A.unsigned_decimal + __PROC_CURRENT_VALUE_B.unsigned_decimal) < 0)
    print(result[0].unsigned_decimal)
    REGISTRY[2] = result[0].copy

def _OP_SUB():
    eprint("SUB", __PROC_CURRENT_VALUE_A.unsigned_decimal, __PROC_CURRENT_VALUE_B.unsigned_decimal)
    result = REGISTRY[__PROC_CURRENT_VALUE_A.unsigned_decimal].copy.SUBTRACT(REGISTRY[__PROC_CURRENT_VALUE_B.unsigned_decimal].copy)
    assign_flag((__PROC_CURRENT_VALUE_A.unsigned_decimal - __PROC_CURRENT_VALUE_B.unsigned_decimal) > BANDWITH_MAX_NUMBER, result[0].unsigned_decimal == 0, result[2], result[1], (__PROC_CURRENT_VALUE_A.unsigned_decimal - __PROC_CURRENT_VALUE_B.unsigned_decimal) < 0)
    REGISTRY[2] = result[0]

def _OP_MUL():
    eprint("MUL", __PROC_CURRENT_VALUE_A.unsigned_decimal, __PROC_CURRENT_VALUE_B.unsigned_decimal)
    result = REGISTRY[__PROC_CURRENT_VALUE_A.unsigned_decimal].copy.MULTIPLY(REGISTRY[__PROC_CURRENT_VALUE_B.unsigned_decimal].copy)
    assign_flag((__PROC_CURRENT_VALUE_A.unsigned_decimal * __PROC_CURRENT_VALUE_B.unsigned_decimal) > BANDWITH_MAX_NUMBER, result[0].unsigned_decimal == 0, result[2], result[1], (__PROC_CURRENT_VALUE_A.unsigned_decimal * __PROC_CURRENT_VALUE_B.unsigned_decimal) < 0)
    REGISTRY[2] = result[0]

def _OP_DIV():
    eprint("DIV", __PROC_CURRENT_VALUE_A.unsigned_decimal, __PROC_CURRENT_VALUE_B.unsigned_decimal)
    result = REGISTRY[__PROC_CURRENT_VALUE_A.unsigned_decimal].copy.DIVIDE(REGISTRY[__PROC_CURRENT_VALUE_B.unsigned_decimal].copy)
    assign_flag((__PROC_CURRENT_VALUE_A.unsigned_decimal / __PROC_CURRENT_VALUE_B.unsigned_decimal) > BANDWITH_MAX_NUMBER, result.unsigned_decimal == 0, (__PROC_CURRENT_VALUE_A.unsigned_decimal / __PROC_CURRENT_VALUE_B.unsigned_decimal) < 0, False)
    REGISTRY[2] = result[0]

def _OP_CMP():
    assign_flag(
        (__PROC_CURRENT_VALUE_A.unsigned_decimal - __PROC_CURRENT_VALUE_B.unsigned_decimal) > BANDWITH_MAX_NUMBER,
        (__PROC_CURRENT_VALUE_A.unsigned_decimal - __PROC_CURRENT_VALUE_B.unsigned_decimal) == 0,
        (__PROC_CURRENT_VALUE_A.unsigned_decimal - __PROC_CURRENT_VALUE_B.unsigned_decimal) < 0,
        False,
        (__PROC_CURRENT_VALUE_A.unsigned_decimal - __PROC_CURRENT_VALUE_B.unsigned_decimal) < 0
    )

OPERATIONS = {
    0: _OP_NOP,
    1: _OP_HALT,

    2: _OP_MOV,      # Copy from reg of src to reg dest
    3: _OP_SET,      # Set registry src to constant
    4: _OP_MEMSET,   # Set ram address to a constant
    5: _OP_LOAD,     # Load from ram address of src to reg of dest
    6: _OP_STORE,    # Store from reg of src to ram at dest
    7: _OP_LEA,      # Load Effective Address (load the address instead of value)
    8: _OP_RND,      # Randomize without ceiling
    9: _OP_RNDC,     # Randomize with maximum
    10: _OP_RNDS,    # Randomize signed from minimum to maximum
    11: _OP_STORER,  # Store value of reg to ram address of reg value

    # Conditional Jumps
    100: _OP_JMP,      # do Unconditional Jump
    101: _OP_JEZ,      # Read From Flags and do Jump if flag is Zero
    105: _OP_JEQ,      # Read From Flags and do Jump if flag is Equal
    106: _OP_JNE,      # Read From Flags and do Jump if flag is Not Equal
    107: _OP_JMG,      # Read From Flags and do Jump if flag is Greater Than
    108: _OP_JML,      # Read From Flags and do Jump if flag is Less Than,

    200: _OP_OR,
    201: _OP_NOR,
    202: _OP_AND,
    203: _OP_NAND,
    204: _OP_XOR,
    205: _OP_XNOR,
    206: _OP_INC,
    207: _OP_DEC,

    301: _OP_ADD,
    302: _OP_SUB,
    303: _OP_MUL,
    304: _OP_DIV,
    305: _OP_CMP,
}

OPERATION_NAMES = {
    0: "NOP",
    1: "HALT",
    2: "MOV",
    3: "SET",
    4: "MEMSET",
    5: "LOAD",
    6: "STORE",
    7: "LEA",
    8:  "RND",
    9:  "RNDC",
    10: "RNDS",
    11: "STORER",
    100: "JMP",
    101: "JEZ",
    105: "JEQ",
    106: "JNE",
    107: "JMG",
    108: "JML",
    200: "OR",
    201: "NOR",
    202: "AND",
    203: "NAND",
    204: "XOR",
    205: "XNOR",
    206: "INC",
    207: "DEC",
    301: "ADD",
    302: "SUB",
    303: "MUL",
    304: "DIV",
    305: "CMP",
}

def tick():
    global __IS_HALTING
    if __IS_HALTING: return

    global __PROC_CURRENT_INSTRUCTION
    global __PROC_CURRENT_VALUE_A
    global __PROC_CURRENT_VALUE_B

    # Fetch
    REGISTRY[1] = RAM[REGISTRY[0].unsigned_decimal].copy
    # Decode
    __instruction = REGISTRY[1].copy.binary[:__INSTRUCTION_BANDWITH:]
    __value_a = REGISTRY[1].copy.binary[__INSTRUCTION_BANDWITH:((ARCH_BIT_BANDWITH - __INSTRUCTION_BANDWITH) // 2) + __INSTRUCTION_BANDWITH:]
    __value_b = REGISTRY[1].copy.binary[((ARCH_BIT_BANDWITH - __INSTRUCTION_BANDWITH) // 2) + __INSTRUCTION_BANDWITH:ARCH_BIT_BANDWITH:]

    __PROC_CURRENT_INSTRUCTION = Binary.from_binary(__instruction)
    __PROC_CURRENT_VALUE_A = Binary.from_binary(__value_a)
    __PROC_CURRENT_VALUE_B = Binary.from_binary(__value_b)

    # eprint(__PROC_CURRENT_INSTRUCTION.unsigned_decimal, __PROC_CURRENT_VALUE_A.unsigned_decimal, __PROC_CURRENT_VALUE_B.unsigned_decimal)
    # eprint(len(__instruction), len(__value_a), len(__value_b))
    
    try:
        operation = OPERATIONS[__PROC_CURRENT_INSTRUCTION.unsigned_decimal]
        operation_name = OPERATION_NAMES[__PROC_CURRENT_INSTRUCTION.unsigned_decimal]
    except:
        eprint("Operation Not Found!")
        __IS_HALTING = True
        return
    
    operation()
    if operation_name not in ["JMP", "JEZ", "JEQ", "JNE", "JMG", "JML"]:
        REGISTRY[0] = Binary.from_decimal(REGISTRY[0].unsigned_decimal + 1)
    
    # for i in REGISTRY_NAMES:
    #     eprint(REGISTRY_NAMES[i], ":", REGISTRY[i].unsigned_decimal, end=" | ")
    # eprint()
