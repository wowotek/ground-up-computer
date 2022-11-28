import sys
import cpu
import gui

args = sys.argv
if len(args) <= 1:
    print("File Input Missing", file=sys.stderr)
    exit(1)

with open(args[1], "r") as f:
    content = [i.replace("\n", "") for i in f.readlines()]

cpu.initialize_ram([cpu.Binary.from_binary(i) for i in content])

gui.start()