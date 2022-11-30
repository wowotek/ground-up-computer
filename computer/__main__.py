import sys
import cpu

args = sys.argv
if len(args) <= 1:
    print("File Input Missing", file=sys.stderr)
    exit(1)

with open(args[1], "r") as f:
    content = [i.replace("\n", "") for i in f.readlines()]

content = [cpu.Binary.from_binary(i) for i in content]
print("Loading Program To RAM")

cpu.initialize_ram(content, 240, 240)
import gui