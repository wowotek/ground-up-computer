; example program wComputer
"MOV": 100,
"SET": 101,
"SAVE": 120,
"LOAD": 140,
"STORE": 160,
"LEA": 180,

"JMP": 200,
"JMZ": 220,
"JMN": 240,
"JEQ": 260,
"JNE": 280,
"JMG": 300,
"JML": 320,
"NOP": 800,
"HALT": 900,

# ALU
"PASS": 0,
"OR": 1,
"NOR": 2,
"XOR": 3,
"AND": 4,
"NAND": 5,
"ADD": 6,
"SUBTRACT": 7,
"NOT": 8,
"SHIFT_LEFT": 9,
"SHIFT_RIGHT": 10,
"COMPARE": 11,

:SECTION_ONE


    set rga 7382      ; set register RGA to 64

    mov rga rfs     ; move from rga to rgb