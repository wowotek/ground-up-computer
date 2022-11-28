def split_every_nth(target: str, n: int):
    return [target[i:i+n] for i in range(0, len(target), n)]


def full_adder(a: bool, b: bool, carry: bool):
    a_xor_b = a ^ b
    a_and_b = a & b

    a_xor_b_and_carry = a_xor_b & carry


    result = a_xor_b ^ carry
    return bool(result), bool(a_and_b | a_xor_b_and_carry)