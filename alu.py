from binary import Binary, list_to_decimal, interpret_list_with_negative, MAX_VALUE


class ALU:
    def __init__(self):
        self.ARITHMETIC_OPS = {
            0: self._OP_PASS,
            1: self._OP_OR,
            2: self._OP_NOR,
            3: self._OP_XOR,
            4: self._OP_AND,
            5: self._OP_NAND,
            6: self._OP_ADD,
            7: self._OP_SUBTRACT,
            8: self._OP_NOT,
            9: self._OP_SHIFT_LEFT,
            10: self._OP_SHIFT_RIGHT,
            11: self._OP_COMPARE,
        }

        self.input_a = Binary(0)
        self.input_b = Binary(0)
        self.input_op = Binary(0)
        self.input_carry = False

        self.flag_zero = False
        self.flag_overflow = False
        self.flag_carry = False
        self.flag_negative = False

        self.result = Binary(0)
    
    def load_value(self, a: Binary, b: Binary, op: Binary, carry_in: bool = False):
        self.input_a = a.copy()
        self.input_b = b.copy()
        self.input_op = op.copy()
        self.input_carry = carry_in

    def tick(self):
        # Get Arithmetic OPS
        op_decimal = self.input_op.decimal()
        current_op = self._OP_PASS
        if op_decimal in self.ARITHMETIC_OPS:
            current_op = self.ARITHMETIC_OPS[op_decimal]
        
        current_op()

    def _full_adder(self, cin: bool, a: bool, b: bool):
        ab_xor = (a ^ b)
        result = ab_xor ^ cin

        cin_carrier = ab_xor & cin
        ab_carrier = a & b

        cout = cin_carrier | ab_carrier

        return (cout, result)
    
    def _detect_zero(self):
        for i in range(self.result.size()):
            if self.result.get_at(i):
                return False
        
        return True

    def _OP_PASS(self):
        for i in range(self.result.size()):
            pass
    
    def _OP_OR(self):
        self.result = Binary(0)

        for i in range(self.result.size()):
            self.result.set_at(i, self.input_a.get_at(i) or self.input_b.get_at(i))

        self.flag_zero = self._detect_zero()
        self.flag_overflow = False
        self.flag_carry = False
        self.flag_negative = self.result.get_at(0)
    
    def _OP_NOR(self):
        self.result = Binary(0)

        for i in range(self.result.size()):
            self.result.set_at(i, not (self.input_a.get_at(i) or self.input_b.get_at(i)))

        self.flag_zero = self._detect_zero()
        self.flag_overflow = False
        self.flag_carry = False
        self.flag_negative = self.result.get_at(0)

    def _OP_XOR(self):
        self.result = Binary(0)

        for i in range(self.result.size()):
            self.result.set_at(i, self.input_a.get_at(i) ^ self.input_b.get_at(i))
        
        self.flag_zero = self._detect_zero()
        self.flag_overflow = False
        self.flag_carry = False
        self.flag_negative = self.result.get_at(0)
    
    def _OP_AND(self):
        self.result = Binary(0)

        for i in range(self.result.size()):
            self.result.set_at(i, self.input_a.get_at(i) and self.input_b.get_at(i))
        
        self.flag_zero = self._detect_zero()
        self.flag_overflow = False
        self.flag_carry = False
        self.flag_negative = self.result.get_at(0)
    
    def _OP_NAND(self):
        self.result = Binary(0)

        for i in range(self.result.size()):
            self.result.set_at(i, not (self.input_a.get_at(i) and self.input_b.get_at(i)))
        
        self.flag_zero = self._detect_zero()
        self.flag_overflow = False
        self.flag_carry = False
        self.flag_negative = self.result.get_at(0)
    
    def _OP_ADD(self):
        self.result = Binary(0)
        self.flag_carry = False

        _a = self.input_a.copy().reversed()
        _b = self.input_b.copy().reversed()
        result = []

        for i in range(_a.size()):
            r = self._full_adder(self.flag_carry, _a.get_at(i), _b.get_at(i))
            self.flag_carry = r[0]
            result.append(r[1])
        
        result.reverse()

        self.result = Binary(list_to_decimal(result))

        # Overflow Detection
        not_a = not self.input_a.get_last()
        not_b = not self.input_b.get_last()
        not_r = not self.result.get_last()

        and_1 = not_r & self.input_b.get_last() & self.input_a.get_last()
        and_2 = self.result.get_last() & not_a & not_b

        self.flag_zero = self._detect_zero()
        self.flag_overflow = and_1 or and_2
        self.flag_negative = self.result.get_at(0)
    

    """
    Y = A + (~B) + 1
    """
    def _OP_SUBTRACT(self):
        self.result = Binary(0)
        self.flag_carry = True

        _a = self.input_a.reversed()
        _b = self.input_b.self_op_xor(Binary(MAX_VALUE)).reversed() # Invert B
        result = []

        for i in range(_a.size()):
            r = self._full_adder(self.flag_carry, _a.get_at(i), _b.get_at(i))
            self.flag_carry = r[0]
            result.append(r[1])
        
        result.reverse()

        self.result = Binary(list_to_decimal(result))

        # Overflow Detection
        not_a = not self.input_a.get_last()
        not_b = not self.input_b.get_last()
        not_r = not self.result.get_last()

        and_1 = not_r & self.input_b.get_last() & self.input_a.get_last()
        and_2 = self.result.get_last() & not_a & not_b

        self.flag_zero = self._detect_zero()
        self.flag_overflow = and_1 or and_2
        self.flag_negative = self.result.get_at(0)
    
    def _OP_NOT(self):
        self.result = Binary(0)

        r = [not self.input_a.get_at(i) for i in range(self.input_a.size())]

        for i in range(self.result.size()):
            self.result.set_at(i, r[i])

        self.flag_zero = self._detect_zero()
        self.flag_overflow = False
        self.flag_carry = False
        self.flag_negative = self.result.get_at(0)

    def _OP_SHIFT_LEFT(self):
        self.result = Binary(0)

        r = [self.input_a.get_at(i) for i in range(self.input_a.size())]
        r.append(r.pop(0))

        for i in range(self.result.size()):
            self.result.set_at(i, r[i])

        self.flag_zero = self._detect_zero()
        self.flag_overflow = False
        self.flag_carry = False
        self.flag_negative = self.result.get_at(0)

    def _OP_SHIFT_RIGHT(self):
        self.result = Binary(0)

        r = [self.input_a.get_at(i) for i in range(self.input_a.size())]
        r.insert(0, r.pop())

        for i in range(self.result.size()):
            self.result.set_at(i, r[i])

        self.flag_zero = self._detect_zero()
        self.flag_overflow = False
        self.flag_carry = False
        self.flag_negative = self.result.get_at(0)
    
    def _OP_COMPARE(self):
        val = 0 
        if self.input_a < self.input_b:
            val = 1
        elif self.input_a > self.input_b:
            val = 2

        self.result = Binary(val)

        self.flag_zero = self._detect_zero()
        self.flag_overflow = False
        self.flag_carry = False
        self.flag_negative = self.result.get_at(0)
    
    def __str__(self):
        _op = ''.join(["1" if self.input_op.get_at(i) else "0" for i in range(self.input_op.size())])
        input_op =     f"I_OP       = {_op}  |  {interpret_list_with_negative(self.input_op.boolean_list())}"

        _a = ''.join(["1" if self.input_a.get_at(i) else "0" for i in range(self.input_a.size())])
        input_a =      f"I_A        = {_a}  |  {interpret_list_with_negative(self.input_a.boolean_list())}"
        _b = ''.join(["1" if self.input_b.get_at(i) else "0" for i in range(self.input_b.size())])
        input_b =      f"I_B        = {_b}  |  {interpret_list_with_negative(self.input_b.boolean_list())}"

        _r = ''.join(["1" if self.result.get_at(i) else "0" for i in range(self.result.size())])
        result =       f"Y_Result   = {_r}  |  {interpret_list_with_negative(self.result.boolean_list())}"

        flagzero =     f"F_Zero     = {1 if self.flag_zero else 0}"
        flagoverflow = f"F_Overflow = {1 if self.flag_overflow else 0}"
        flagcarry =    f"F_Carry    = {1 if self.flag_carry else 0}"
        flagnegative = f"F_Negative = {1 if self.flag_negative else 0}"

        return "\n--------ALU-State----------\n" + input_a + "\n" + input_b + "\n" + input_op + "\n-----\n" + result + "\n----\n" + flagzero + "\n" + flagoverflow + "\n" + flagcarry + "\n" + flagnegative
    
    def __repr__(self):
        return self.__str__()

a = ALU()
print(a)
a.load_value(Binary(128), Binary(127), Binary(6)) 
print(a)
a.tick()
print(a)