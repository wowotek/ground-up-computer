from binary import Binary, list_to_decimal, decimal_to_list

from alu import ALU
from ram import RAM


class CPU:
    def __init__(self, ram: RAM):
        self.ALU_OP_CODES = [i for i in range(11)]
        self.CPU_OPS = {
            # Memory And Register Operations
            32: self._OP_MOV_A,      # Move from register to registers A
            33: self._OP_MOV_B,      # Move from register to registers B
            34: self._OP_MOV_C,      # Move from register to registers C
            35: self._OP_MOV_D,      # Move from register to registers D
            36: self._OP_MOV_E,      # Move from register to registers E
            40: self._OP_MOV_MEM,    # Move from register to register memory

            40: self._OP_LOAD,     # Load from stack (ram) to memory register
            41: self._OP_STORE,    # Store from memory register to stack address
            42: self._OP_LEA,      # Load Effective Address (load the address instead of value)

            # Conditional Jumps
            43: self._OP_JUMP,     # Unconditional Jump
            44: self._OP_JMZ,      # Jump Zero
            45: self._OP_JMN,      # Jump Negative
            46: self._OP_JEQ,      # Jump Equal
            47: self._OP_JNE,      # Jump Not Equal
            48: self._OP_JMG,      # Jump Greater Than
            49: self._OP_JML,      # Jump Less Than,

            62: self._OP_NOP,      # No Operation
            63: self._OP_HALT      # Halt CPU
        }

        # Hardware
        self._ram = ram
        self._alu = ALU()

        # Functional Registers

        self.reg_stack_counter = Binary(0) # stack_counter
        self.reg_instruction = Binary(0) # instruction
        self.reg_memory = Binary(0) # memory -- Every Memory Register Operation require this register
        self.reg_a = Binary(0) # a -- Also ALU Input A
        self.reg_b = Binary(0) # b -- Also ALU Input B
        self.reg_c = Binary(0) # c -- Also ALU Return
        self.reg_d = Binary(0) # d
        self.reg_e = Binary(0) # e


        self.__current_phase = 0
        self.__current_operation: list[bool] = []
        self.__current_value: list[bool] = []
        
        self.__is_halting = False
    
    def tick(self):
        if self.__is_halting: return

        if self.__current_phase == 0:     # Fetch
            self._phase_fetch()
        elif self.__current_phase == 1:   # Decode
            self._phase_decode()
        elif self.__current_phase == 2:   # Execute
            self._phase_execute()
        
        self.__current_phase += 1
        if self.__current_phase >= 2: self.__current_phase = 0
    
    def _phase_fetch(self):
        self._ram.load_value(self.reg_stack_counter)
        self._ram.tick()
        self.reg_instruction = self._ram.data_io
    
    def _phase_decode(self):
        self.__current_operation = decimal_to_list(self.reg_instruction.decimal)[:8]
        self.__current_value = decimal_to_list(self.reg_instruction.decimal)[-(self.reg_instruction.size()-8)::]
    
    def _phase_execute(self):
        op_decimal = list_to_decimal(self.__current_operation)
        if op_decimal in self.ALU_OP_CODES:
            raise NotImplementedError()
        elif op_decimal in [key for key in self.CPU_OPS]:
            self.CPU_OPS[op_decimal]()

        self.reg_stack_counter = Binary(self.reg_stack_counter.decimal + 1)
    
    def __split_value(self, bit_lengths: list[int]):
        bit_length_sum = sum(bit_lengths)
        if bit_length_sum > len(self.__current_value):
            raise AssertionError("value split valied, bit_length_sum is more than value bit length")
        
        last_bit_index = 0
        result = []
        for i in bit_lengths:
            result.append(self.__current_value[last_bit_index:last_bit_index+i:])
            last_bit_index = i
        
        return tuple(result)
        
    def _OP_MOV(self):
        operands = self.__split_value([int(len(self.__current_value)/2), int(len(self.__current_value)/2)])
    def _OP_LOAD(self): pass
    def _OP_STORE(self): pass
    def _OP_LEA(self): pass

    def _OP_JUMP(self): pass
    def _OP_JMZ(self): pass
    def _OP_JMN(self): pass
    def _OP_JEQ(self): pass
    def _OP_JNE(self): pass
    def _OP_JMG(self): pass
    def _OP_JML(self): pass

    def _OP_NOP(self): pass
    def _OP_HALT(self): self.is_halting = True