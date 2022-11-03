from binary import Binary, BIT_LENGTH


class RAM:
    def __init__(self, number_of_bit_length: int):
        self._ram = {}

        for i in range(number_of_bit_length):
            self._ram[i] = Binary(0)

        self.input_address = Binary(0)
        self.read_enable = False
        self.write_enable = False
        self.data_io = Binary(0)
        
        print(f"Initialized RAM with {(number_of_bit_length * BIT_LENGTH) / 8} byte")
        print(self._ram)
    
    def load_value(self, input_address: Binary, is_read: bool, data: Binary):
        self.input_address = input_address.copy()
        self.data_io = data
        if is_read:
            self.read_enable = True
            self.write_enable = False
        else:
            self.read_enable = False
            self.write_enable = True
    
    def tick(self):
        if self.read_enable:
            self.data_io = self._get_from_ram(self.input_address)

        if self.write_enable:
            self._set_to_ram(self.input_address, self.data_io)
        
        self.input_address = Binary(0)
        self.read_enable = False
        self.write_enable = False
        self.data_io = Binary(0)

    def _get_from_ram(self, address: int):
        if address > len(self._ram):
            raise IndexError("Requested Address More than installed ram")
        
        return self._ram[address]
    
    def _set_to_ram(self, address: int, value: Binary):
        if address > len(self._ram):
            raise IndexError("Requested Address More than installed ram")
        
        self._ram[address] = value