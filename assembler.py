OPERATION_VALUES = {
    "NOP"   : 0,
    "HALT"  : 1,
    "MOV"   : 2,
    "SET"   : 3,
    "MEMSET": 4,
    "LOAD"  : 5,
    "STORE" : 6,
    "LEA"   : 7,
    "JMP"   : 100,
    "JEZ"   : 101,
    "JGZ"   : 102,
    "JLZ"   : 103,
    "JMN"   : 104,
    "JEQ"   : 105,
    "JNE"   : 106,
    "JMG"   : 107,
    "JML"   : 108,
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
    "JMP"   : ["RAM"],
    "JEZ"   : ["RAM"],
    "JGZ"   : ["RAM"],
    "JLZ"   : ["RAM"],
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

PROGRAM = {}
JMP_ADDRESES = {}
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
        JMP_ADDRESES[i.replace(":", "")] = count

####################################################################################
####################################################################################

# Check if Any Written Operand is not defined
for i in PROGRAM:
    if PROGRAM[i][0] not in [i for i in OPERATION_VALUES]: raise Exception(f"Operator of {PROGRAM[i][0]} Does Not Exist")


# Parse Jumps and/or Branches Control
for i in PROGRAM:
    if PROGRAM[i][0] in ["JMP", "JEZ", "JGZ", "JLZ", "JMN", "JEQ", "JNE", "JMG", "JML"]:
        if PROGRAM[i][1] not in JMP_ADDRESES: raise Exception(f"SUBSECTION {PROGRAM[i][1]} does not exist")
    
        PROGRAM[i][1] = JMP_ADDRESES[PROGRAM[i][1]]

for i in PROGRAM:
    ops = PROGRAM[i][0]
    if ops not in [i for i in OPERATION_VALUES]: raise Exception(f"OPERATOR {i} not Found")

    PROGRAM[i][0] = OPERATION_VALUES[ops]

print(PROGRAM)
print(JMP_ADDRESES)