import enum

DIRECTIVES = {".ORIG", ".FILL", ".BLKW", ".STRINGZ", ".END"}
OPCODES = {
    # Basic ALU & Memory
    "ADD", "AND", "NOT",
    "LD", "LDI", "LDR", "LEA",
    "ST", "STI", "STR",
    # Control flow
    "BR", "BRN", "BRZ", "BRP", "BRNZ", "BRNP", "BRZP", "BRNZP",
    "JMP", "JSR", "JSRR", "RET", "RTI",
    # Traps (LC-3 treats these pseudo-ops as opcodes)
    "TRAP", "HALT", "GETC", "OUT", "PUTS", "IN", "PUTSP"
}

class token_type(enum.Enum):
    DIR='DIR' # directive
    STR='STR' # string
    COM='COM' # comment
    NUM='NUM' # number
    REG='REG' # register
    OPS='OPS' # opcode
    LBL='LBL' # label

def tokenize(kind: str, name: str):
    print(f'{kind}: |{name}|')

def tokenize_line(line: str):
    n = len(line)
    i = 0
    while i < n:
        c = line[i]
        if c == ';':
            break
        if c in ' \t,':
            i+=1
        if c == '.':
            beg=i
            i+=1
            while i < n and (line[i].isalnum() or line[i] == '_'):
                i+=1
            tokenize(token_type.DIR, line[beg:i])
            continue

        if c in '#xX':
            beg=i
            i+=1
            while i < n and (line[i].isalnum() or line[i] == '-'):
                i+=1
            tokenize(token_type.NUM, line[beg:i])
            continue

        if c == '"':
            beg=i
            i+=1
            while i < n and line[i] != '"':
                i+=1
            tokenize(token_type.STR, line[beg:i+1])
            i+=1
            continue

        if c.isalnum() or c == '_':
            beg=i
            i+=1
            while i < n and (line[i].isalnum() or line[i] == '_'):
                i+=1
            token=line[beg:i].upper()
            if (i - beg) == 2 and token[0] == 'R' and token[1] in '01234567':
                tokenize(token_type.REG, line[beg:i])
            elif token in OPCODES:
                tokenize(token_type.OPS, token)
            else:
                tokenize(token_type.LBL, token)
            continue

with open('tests/tokenizer_test.asm', 'r') as file:
    for line in file:
        tokenize_line(line.strip())
