import os

SYMBOL_TABLE = {'R0': 0, 'R1': 1, 'R2': 2, 'R3': 3, 'R4': 4, 'R5': 5, 'R6': 6, 'R7': 7, 'R8': 8, 'R9': 9, 'R10': 10, 'R11': 11, 'R12': 12, 'R13': 13, 'R14': 14,
                'R15': 15,
                'SCREEN': 16384, 'KBD': 24579, 'SP': 0, 'LCL': 1, 'ARG': 2, 'THIS': 3, 'THAT': 4}
JUMP_TABLE = {'': '000', 'JGT': '001', 'JEQ': '010', 'JGE': '011', 'JLT': '100', 'JNE': '101', 'JLE': '110', 'JMP': '111'}
DEST_TABLE = {'': '000', 'M': '001', 'D': '010', 'MD': '011', 'A': '100', 'AM': '101', 'AD': '110', 'AMD': '111'}
COMP_TABLE = {'0': '0101010',
              '1': '0111111',
              '-1': '0111010',
              'D': '0001100',
              'A': '0110000', 'M': '1110000',
              '!D': '0001101',
              '!A': '0110001', '!M': '1110001',
              '-D': '0001111',
              '-A': '0110011', '-M': '1110011',
              'D+1': '0011111',
              'A+1': '0110111', 'M+1': '1110111',
              'D-1': '0001110',
              'A-1': '0110010', 'M-1': '1110010',
              'D+A': '0000010', 'D+M': '1000010',
              'D-A': '0010011', 'D-M': '1010011',
              'A-D': '0000111', 'M-D': '1000111',
              'D&A': '0000000', 'D&M': '1000000',
              'D|A': '0010101', 'D|M': '1010101',
              '':''}
labels = {}
vars = {}
binaryCode = []
code = []
newCode = []

os.chdir(r"W:\Dropbox\_myRepoGitHub\from_NAND_to_tetris\nand2tetris\projects\06\pong")
file = open('Pong.asm', "r")


def printCode(code):
    counter = 0
    for line in code:
        # print str(counter) + " " + line
        print line
        counter += 1
    print


# remove comments and other
def removeComments():
    global code
    for line in file:
        if not (str(line).startswith("//") or str(line).startswith("\n")):
            code.append(line.replace('\n', "").split("//", 1)[0].strip())


# replace predefine variables
def replacePreDefine():
    global code, newCode
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
def replaceLabels():
    global code, newCode
    counter = 0
    newCode = []
    for line in code:
        if str(line).startswith("("):
            line = line[1:-1]
            labels[line] = counter  # + 1
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
def replaceVariables():
    global code, newCode
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

# convert decimal to binary
get_bin = lambda x, n: x >= 0 and str(bin(x))[2:].zfill(n) or "-" + str(bin(x))[3:].zfill(n)

# translate A and C instruction
def compile_A_Instruction(line):
    return "0" + get_bin(int(line[1:]), 15)


def comp(key):
    res = COMP_TABLE[key]
    return res


def dest(key):
    res = DEST_TABLE[key]
    return res


def jump(key):
    res = JUMP_TABLE[key]
    return res


def compile_C_Instruction(line):
    dIns = ""
    cIns = ""
    jIns = ""
    if line.find(";") > 0:
        res = line.split(";")
        jIns = res[1]
        cIns = res[0]
        line = res[0]
    if line.find("=") > 0:
        res = line.split("=")
        cIns = res[1]
        dIns = res[0]
    return "111" + comp(cIns) + dest(dIns) + jump(jIns)


def compile():
    global binaryCode
    for line in code:
        if str(line).startswith("@"):
            line = compile_A_Instruction(line)
        else:
            line = compile_C_Instruction(line)
        binaryCode.append(line)

# start
removeComments()
replacePreDefine()
replaceLabels()
replaceVariables()
compile()

#printCode(code)
print
printCode(binaryCode)

# print str('0' + get_bin(21,15))