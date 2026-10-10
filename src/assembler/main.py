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
    
token_list = []
symbol_table = {}

PC=0x3000
LC=0x0000

def get_token(kind: str, name: str):
    return (kind,name)

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
            token_list.append(get_token(token_type.DIR, line[beg:i]))
            continue

        if c in '#xX':
            beg=i
            i+=1
            while i < n and (line[i].isalnum() or line[i] == '-'):
                i+=1
            token_list.append(get_token(token_type.NUM, line[beg:i]))
            continue

        if c == '"':
            beg=i
            i+=1
            while i < n and line[i] != '"':
                i+=1
            token_list.append(get_token(token_type.STR, line[beg:i+1]))
            i+=1
            continue

        if c.isalnum() or c == '_':
            beg=i
            i+=1
            while i < n and (line[i].isalnum() or line[i] == '_'):
                i+=1
            token=line[beg:i].upper()
            if (i - beg) == 2 and token[0] == 'R' and token[1] in '01234567':
                token_list.append(get_token(token_type.REG, line[beg:i]))
            elif token in OPCODES:
                token_list.append(get_token(token_type.OPS, token))
            else:
                token_list.append(get_token(token_type.LBL, token))
            continue

with open('tests/label_test.asm', 'r') as file:
    for line in file:
        tokenize_line(line.strip())

    n = len(token_list)
    i = 0
    while i < n:
        ttype, value = token_list[i]
        # print(f'type: {ttype}, value: {value}, LC: {hex(LC)}')
        i+=1

        if ttype == token_type.DIR and value == '.ORIG':
            _,h=token_list[i]
            h='0'+h
            LC=int(h,16)
            continue

        if (ttype == token_type.DIR and value == '.FILL') or ttype == token_type.OPS:
            LC+=1
            continue

        if ttype == token_type.DIR and value == '.BLKW':
            _,value=token_list[i]
            value = int(value[1:])
            LC=LC+value
            continue

        if ttype == token_type.DIR and value == '.STRINGZ':
            _,value=token_list[i]
            LC=LC+len(value[1:-1])+1
            continue

        if ttype == token_type.DIR and value == '.END':
            break

        if ttype == token_type.LBL:
            symbol_table[value] = hex(LC)
            continue

    print(symbol_table)


