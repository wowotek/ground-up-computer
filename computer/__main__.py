import sys
import cpu

args = sys.argv
if len(args) <= 1:
    print("File Input Missing", file=sys.stderr)
    exit(1)

with open(args[1], "r") as f:
    content = [i.replace("\n", "") for i in f.readlines()]

for i in content:
    print(i)
content = [cpu.Binary.from_binary(i) for i in content]
print("Loading Program To RAM with content of :")
[print("    ", i) for i in content]

cpu.initialize_ram(content)
import gui