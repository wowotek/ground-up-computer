def split_every_nth(target: str, n: int):
    return [target[i:i+n] for i in range(0, len(target), n)]

def binaryToReadableHex(binary: str, sep: str = " "):
    arc_len = 256
    ins_len = 10
    _instruction = binary[:ins_len:]
    _value_a = binary[ins_len:((arc_len - ins_len) // 2) + ins_len:]
    _value_b = binary[((arc_len - ins_len) // 2) + ins_len:arc_len:]

    maxins = len(hex(int("".join(["1" for _ in range(len(_instruction))]), 2)).replace("0x", ""))
    maxval = len(hex(int("".join(["1" for _ in range(len(_value_a))]), 2)).replace("0x", ""))

    ins = hex(int(_instruction, 2)).replace("0x", "").rjust(maxins, "0")
    va = hex(int(_value_a, 2)).replace("0x", "").rjust(maxval, "0")
    vb = hex(int(_value_b, 2)).replace("0x", "").rjust(maxval, "0")

    return sep.join([ins, va, vb])

def map_value(original_start: float, original_end: float, mapped_start: float, mapped_end: float, value: float):
    return mapped_start + ((mapped_end - mapped_start) / (original_end - original_start)) * (value - original_start)

def full_adder(a: bool, b: bool, carry: bool):
    a_xor_b = a ^ b
    a_and_b = a & b

    a_xor_b_and_carry = a_xor_b & carry


    result = a_xor_b ^ carry
    return bool(result), bool(a_and_b | a_xor_b_and_carry)