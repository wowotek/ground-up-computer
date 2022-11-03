from binary import Binary, decimal_to_list

from alu import ALU
from ram import RAM


class CPU:
    def __init__(self, ram: RAM):
        self.CPU_OPS = {
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
        }

        self.ram = ram
        self.alu = ALU()
        self.reg_instruction_counter = Binary(0)
        self.reg_instruction = Binary(0)

        self.reg_a = Binary(0)
        self.reg_b = Binary(0)
        self.reg_c = Binary(0)
        self.reg_d = Binary(0)

        self.current_phase = 0
        self.current_operation: list[bool] = []
        self.current_value: list[bool] = []
    
    def tick(self):
        if self.current_phase == 0:
            # fetch
            self.ram.load_value(self.reg_instruction_counter)
            self.reg_instruction = self.ram.data_io
        elif self.current_phase == 1:
            # decode
            self.current_operation = decimal_to_list(self.reg_instruction.decimal)[:6]
            self.current_value = decimal_to_list(self.reg_instruction.decimal)[-(self.reg_instruction.size()-6)::]
            print("op", self.current_operation, " |  val", self.current_value)
        elif self.current_phase == 2:
            # execute
            
            
            # add one to Program Counter
            self.reg_instruction_counter = Binary(self.reg_instruction_counter.decimal + 1)
        
        self.current_phase += 1
        if self.current_phase >= 2: self.current_phase = 0