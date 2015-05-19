import os

SYMBOL_TABLE = {'R0': 0, 'R1': 1, 'R2': 2, 'R3': 3, 'R4': 4, 'R5': 5, 'R6': 6, 'R7': 7, 'R8': 8, 'R9': 9, 'R10': 10, 'R11': 11, 'R12': 12, 'R13': 13, 'R14': 14,
                'R15': 15,
                'SCREEN': 16384, 'KBD': 24579, 'SP': 0, 'LCL': 1, 'ARG': 2, 'THIS': 3, 'THAT': 4}
labels = {}
vars = {}
code = []
newCode = []

os.chdir(r"W:\Dropbox\_myRepoGitHub\from_NAND_to_tetris\nand2tetris\projects\06\pong")
file = open('Pong.asm', "r")


def printCode():
    counter = 0
    for line in code:
        # print str(counter) + " " + line
        print line
        counter += 1
    print

# remove comments and other
for line in file:
    if not (str(line).startswith("//") or str(line).startswith("\n")):
        code.append(line.replace('\n', "").split("//", 1)[0].strip())

# replace predefine variables
counter = 0
newCode = []
for line in code:
    if str(line).startswith("@"):
        key = line[1:]
        if SYMBOL_TABLE.has_key(key):
            line = line.replace(key, str(SYMBOL_TABLE[key]))
    newCode.append(line)
    counter += 1
code = newCode

# replace labels
counter = 0
newCode = []
for line in code:
    if str(line).startswith("("):
        line = line[1:-1]
        labels[line] = counter #+ 1
    else:
        newCode.append(line)
        counter += 1
code = newCode

counter = 0
newCode = []
for line in code:
    if str(line).startswith("@"):
        key = line[1:]
        if labels.has_key(key):
            line = line.replace(key, str(labels[key]))
    newCode.append(line)
    counter += 1
code = newCode

# replace variables
counter = 16
for line in code:
    if str(line).startswith("@"):
        line = line[1:]
        if not line.isdigit():
            if not vars.has_key(line):
                vars[line] = counter
                counter += 1

counter = 0
newCode = []
for line in code:
    if str(line).startswith("@"):
        key = line[1:]
        if vars.has_key(key):
            line = line.replace(key, str(vars[key]))
    newCode.append(line)
    counter += 1
code = newCode

# translate asm to binary code

printCode()