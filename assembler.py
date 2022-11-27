OPERATION_VALUES = {
    "NOP"   : 0,
    "HALT"  : 1,
    "MOV"   : 2,
    "SET"   : 3,
    "MEMSET": 4,
    "LOAD"  : 5,
    "STORE" : 6,
    "LEA"   : 7,
    "JUMP"  : 100,
    "JMZ"   : 101,
    "JMN"   : 102,
    "JEQ"   : 103,
    "JNE"   : 104,
    "JMG"   : 105,
    "JML"   : 106,
    "OR"    : 200,
    "NOR"   : 201,
    "AND"   : 202,
    "NAND"  : 203,
    "XOR"   : 204,
    "XNOR"  : 205,
    "ADD"   : 301,
    "SUB"   : 302,
    "MUL"   : 303,
    "DIV"   : 304,
    "CMP"   : 305,
}

OPERATION_OPERANDS = {
    "NOP"   : [],
    "HALT"  : [],
    "MOV"   : ["REG", "REG"],
    "SET"   : ["REG", "CONST"],
    "MEMSET": ["RAM" "CONST"],
    "LOAD"  : ["RAM", "REG"],
    "STORE" : ["REG", "RAM"],
    "LEA"   : ["RAM", "REG"],
    "JUMP"  : ["RAM"],
    "JMZ"   : ["RAM"],
    "JMN"   : ["RAM"],
    "JEQ"   : ["RAM"],
    "JNE"   : ["RAM"],
    "JMG"   : ["RAM"],
    "JML"   : ["RAM"],
    "OR"    : ["REG", "REG"],
    "NOR"   : ["REG", "REG"],
    "AND"   : ["REG", "REG"],
    "NAND"  : ["REG", "REG"],
    "XOR"   : ["REG", "REG"],
    "XNOR"  : ["REG", "REG"],
    "ADD"   : ["REG", "REG"],
    "SUB"   : ["REG", "REG"],
    "MULY"  : ["REG", "REG"],
    "DIV"   : ["REG", "REG"],
    "CMP"   : ["REG", "REG"],
}

PROGRAM = {}
JUMP_ADDRESES = {}
with open("contoh_program.asm", "r") as f:
    contents = f.readlines()
    contents = [" ".join([k for k in j.split(" ") if k != ""]) for j in [i.replace("\n", "") for i in contents if i[0] != ";"] if j != ""]
    contents = [i.split(";", 1)[0] for i in contents]
    contents = [i.rstrip() for i in contents]

count = 0
for i in contents:
    if i[0] != ":":
        PROGRAM[count] = [i.upper() for i in i.split(" ")]
        count += 1
    else:
        JUMP_ADDRESES[i.replace(":", "")] = count

for i in PROGRAM:
    ops = PROGRAM[i][0]
    if ops not in [i for i in OPERATION_VALUES]: raise Exception(f"OPERATOR {i} not Found")

    PROGRAM[i][0] = OPERATION_VALUES[ops]
print(PROGRAM)
print(JUMP_ADDRESES)