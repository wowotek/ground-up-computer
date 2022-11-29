import sys, pygame
import random
import utils
import time

import cpu

OPERATION_OPERANDS: dict[str, list[str]] = {
    "NOP"   : [],
    "HALT"  : [],
    "MOV"   : ["REG", "REG"],
    "SET"   : ["REG", "CONST"],
    "MEMSET": ["RAM" "CONST"],
    "LOAD"  : ["RAM", "REG"],
    "STORE" : ["REG", "RAM"],
    "LEA"   : ["RAM", "REG"],
    "RND"   : ["REG"],
    "RNDC"  : ["REG"],
    "RNDS"  : ["REG", "CONST"],
    "STORER": ["REG", "REG"],
    "JMP"   : ["RAM"],
    "JEZ"   : ["RAM"],
    "JGZ"   : ["RAM"],
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
    "INC"   : ["REG"],
    "DEC"   : ["REG"],
    "ADD"   : ["REG", "REG"],
    "SUB"   : ["REG", "REG"],
    "MULY"  : ["REG", "REG"],
    "DIV"   : ["REG", "REG"],
    "CMP"   : ["REG", "REG"],
}

print("\n"*3)
pygame.init()
pygame.font.init()

size = width, height = 1600, 900
canvas_size = cwidth, cheight = 1600 - 515, 899
vsize = vwidth, vheight = 320, 320
screen = pygame.display.set_mode(size, vsync=0)

label_font = pygame.font.SysFont("Courier", 15)
value_font = pygame.font.SysFont("Courier", 12)

register_names = [cpu.REGISTRY_NAMES[i] for i in cpu.REGISTRY_NAMES]
register_labels = [ label_font.render(i + ":", False, (200, 200, 200))
    for i in register_names
]

def draw_to_screen(color: tuple[int, int, int] | tuple[int, int, int, int], coordinate: tuple[float, float]):
    newx = int(utils.map_value(0, vwidth, 517, cwidth + 514, coordinate[0]))
    newy = int(utils.map_value(0, vheight, 2, cheight - 1, coordinate[1]))
    screen.set_at((newx, newy), color)
    screen.set_at((newx, newy+1), color)
    screen.set_at((newx+1, newy), color)
    screen.set_at((newx+1, newy+1), color)
    screen.set_at((newx, newy+2), color)
    screen.set_at((newx+2, newy), color)
    screen.set_at((newx+2, newy+2), color)
    screen.set_at((newx+1, newy+2), color)
    screen.set_at((newx+2, newy+1), color)
    screen.set_at((newx+3, newy), color)
    screen.set_at((newx+3, newy+1), color)
    screen.set_at((newx+3, newy+2), color)

text_box_data = [
    "" for _ in range(48)
]

def add_to_text_box(data: str):
    text_box_data.append(data)
    if len(text_box_data) > 48:
        text_box_data.pop(0)

pygame.display.flip()
lt = time.time()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    pygame.draw.rect(screen, (15, 15, 15), (0, 0, 515, height))
    pygame.draw.line(screen, (255, 255, 255), (0, 0), (0, height), 1)
    pygame.draw.line(screen, (255, 255, 255), (515, 0), (515, height), 1)
    pygame.draw.line(screen, (255, 255, 255), (width-1, 0), (width-1, height), 1)
    pygame.draw.line(screen, (255, 255, 255), (0, 0), (width, 0), 1)
    pygame.draw.line(screen, (255, 255, 255), (0, height-1), (width, height-1), 1)

    # Register Labels
    [ screen.blit(register_labels[i], (2, (i * 15) - 1))
        for i in range(len(register_labels))
    ]

    # Separator Between Register Labels and Value
    [ pygame.draw.line(screen, (255, 255, 255), (0, (i * 15)), (515, (i * 15)), 1)
        for i in range(len(register_labels)+1)
    ]

    # Draw Text Box Data inside textbox
    for i in range(48):
        if i < len(text_box_data):
            d = str(47-i).rjust(2, "0") + " | " + text_box_data[i]
            if len(d) > 73:
                d = str(47-i).rjust(2, "0") + " | " + text_box_data[i][0:70]
            bgcolor = (15, 15, 15)
            if i == 47:
                bgcolor = (255, 15, 15)
            screen.blit(value_font.render(d.ljust(73, " "), False, (255, 255, 255), bgcolor), (3, (i * 14) + 182))
        else:
            screen.blit(value_font.render("---", False, (255, 255, 255)), (3, (i * 14) + 182))
    
    
    # Show CPU Register Values
    for i in cpu.REGISTRY_NAMES:
        # print(cpu.REGISTRY_NAMES[i], utils.binaryToReadableHex(cpu.REGISTRY[i].binary))
        if cpu.REGISTRY_NAMES[i] in ["RFP", "RFI", "RFR"]:
            screen.blit(
                value_font.render(
                    utils.binaryToReadableHex(cpu.REGISTRY[i].binary),
                    False,
                    (255, 255, 255)
                ),
                (42, (i * 15) + 2)
            )
        elif cpu.REGISTRY_NAMES[i] in ["RFF"]:
            pass
        else:
            screen.blit(
                value_font.render(
                    "".join(utils.split_every_nth(hex(cpu.REGISTRY[i].unsigned_decimal).replace("0x", ""), 2)),
                    False,
                    (255, 255, 255)
                ),
                (42, (i * 15) + 2)
            )

    if len(cpu.RAM) - cpu.PROGRAM_LENGTH >= (vwidth * vheight):
        for i in range(vwidth * vheight):
            decimal = cpu.RAM[cpu.PROGRAM_LENGTH + i].unsigned_decimal
            if decimal == 0: continue

            binary = cpu.RAM[cpu.PROGRAM_LENGTH + i].binary
            r = utils.map_value(0, (2 ** 10)-1, 0, 255, int(binary[0:10], 2)) 
            g = utils.map_value(0, (2 ** 10)-1, 0, 255, int(binary[10:20], 2))
            b = utils.map_value(0, (2 ** 10)-1, 0, 255, int(binary[20:30], 2))
            a = utils.map_value(0, (2 ** 10)-1, 0, 255, int(binary[30:40], 2))

            draw_to_screen((r, g, b), (int(i / vheight), int(i % vheight)))


    pygame.display.flip()

    # add instruction to textbox
    now = time.time()
    if now - lt > 0:
        try:
            instruction = cpu.OPERATION_NAMES[cpu.__PROC_CURRENT_INSTRUCTION.unsigned_decimal]
            instruction_operand_type = OPERATION_OPERANDS[instruction]
            operand = [cpu.__PROC_CURRENT_VALUE_A.unsigned_decimal, cpu.__PROC_CURRENT_VALUE_B.unsigned_decimal]
            for i in range(len(instruction_operand_type)):
                if instruction_operand_type[i] == "REG":
                    operand[i] = cpu.REGISTRY_NAMES[operand[i]]
                
            add_to_text_box(" ".join([instruction.ljust(6, " ")] + [str(i).rjust(3, " ").ljust(6, " ") for i in operand]))
        except: pass
        cpu.tick()
        lt = now