from __future__ import annotations


def list_to_decimal(l: list[bool]) -> int:
    r = []
    for i in l:
        if i == True:
            r.append("1")
        else:
            r.append("0")

    return int("0b" + "".join(r), 2)

def decimal_to_list(decimal: int) -> list[bool]:
    _b = format(decimal, f"0{BIT_LENGTH}b")
    return [True if i == "1" else False for i in _b]



BIT_LENGTH = 8
MAX_VALUE = list_to_decimal([True for _ in range(BIT_LENGTH)])

class Binary:
    def __init__(self, decimal: int = 0):
        _b = format(decimal, f"0{BIT_LENGTH}b")

        if len(_b) > BIT_LENGTH:
            raise AssertionError("Bit Length over 64")

        self._binary = [True if i == "1" else False for i in _b]

    def get_at(self, index: int):
        if index > BIT_LENGTH - 1:
            raise IndexError("Index is over 63")
        
        return self._binary[index]
    
    def set_at(self, index: int, set_value: bool):
        if index > BIT_LENGTH - 1:
            raise IndexError("Index is over 63")
        
        self._binary[index] = set_value
    
    def get_last(self):
        return self.get_at(self.size() - 1)

    def decimal(self):
        s = ["0", "b"]
        for i in self._binary:
            s.append("1" if i == True else "0")
        
        return int("".join(s), 2)

    def size(self):
        return len(self._binary)
    

    def copy(self):
        return Binary(self.decimal())
    
    def reversed(self):
        c = self.copy()
        ac = []

        for i in range(c.size()):
            ac.append(c.get_at(i))
        
        ac.reverse()
        
        a = "0b" + "".join(["1" if i else "0" for i in ac])

        return Binary(int(a, 2))
    
    def self_op_not(self):
        r = [False if self.get_at(i) == True else True for i in range(self.size())]
        x = list_to_decimal(r)
        return Binary(x)
    
    def self_op_and(self, other: Binary):
        r = []

        for i in range(self.size()):
            r.append(self.get_at(i) and other.get_at(i))
        
        return Binary(list_to_decimal(r))
    
    def self_op_or(self, other: Binary):
        r = []
        for i in range(self.size()):
            r.append(self.get_at(i) | other.get_at(i))

        return Binary(list_to_decimal(r))
    
    def self_op_xor(self, other: Binary):
        r = []
        for i in range(self.size()):
            r.append(self.get_at(i) ^ other.get_at(i))

        return Binary(list_to_decimal(r))
    
    def self_op_self_or(self):
        for i in range(self.size()):
            print(i, end="")
            if self.get_at(i):
                return True
        return False
    
    def __str__(self):
        a = []
        for i in range(self.size()):
            a.append("1" if self.get_at(i) else "0")
        
        return "".join(a) + f" | {list_to_decimal(a)}"
    
    def __repr__(self) -> str:
        return self.__str__()