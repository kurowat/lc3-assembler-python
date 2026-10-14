from common import TokenType, DIRECTIVES

LAYOUTS = {
    ("ADD",      "RRR") : (0x1000,[(9,3),(6,3),(0,3)]),
    ("ADD",      "RRN") : (0x1020,[(9,3),(6,3),(0,5)]),
    ("AND",      "RRR") : (0x5000,[(9,3),(6,3),(0,3)]),
    ("AND",      "RRN") : (0x5020,[(9,3),(6,3),(0,5)]),
    ("BR",       "L")   : (0x0000,[(0,9)]),
    ("JMP",      "R")   : (0xc000,[(6,3)]),
    ("JSR",      "L")   : (0x4800,[(0,11)]),
    ("JSRR",     "R")   : (0x4000,[(6,3)]),
    ("LD",       "RL")  : (0x2000,[(9,3),(0,9)]),
    ("LDI",      "RL")  : (0xa000,[(9,3),(0,9)]),
    ("LDR",      "RRN") : (0x6000,[(9,3),(6,3),(0,6)]),
    ("LEA",      "RL")  : (0xe000,[(9,3),(0,9)]),
    ("NOT",      "RR")  : (0x903f,[(9,3),(6,3)]),
    ("RET",      "")    : (0xc1c0,[()]),
    ("RTI",      "")    : (0x8000,[()]),
    ("ST",       "RL")  : (0x3000,[(9,3),(0,9)]),
    ("STI",      "RL")  : (0xb000,[(9,3),(0,9)]),
    ("STR",      "RRN") : (0x7000,[(9,3),(6,3),(0,6)]),
    ("TRAP",     "N")   : (0xf000,[(0,8)]),
    ("GETC",     "")    : (0xf020,[()]),
    ("OUT",      "")    : (0xf021,[()]),
    ("PUTS",     "")    : (0xf022,[()]),
    ("IN",       "")    : (0xf023,[()]),
    ("PUTSP",    "")    : (0xf024,[()]),
    ("HALT",     "")    : (0xf025,[()]),
    ("NOP",      "")    : (0x0000,[()]),
}

def _get_layout(operands : list):
    layout=""
    for opd in operands:
        if opd.type == TokenType.REGISTER: layout+='R'
        elif opd.type == TokenType.NUMBER: layout+='N'
        elif opd.type == TokenType.IDENT:  layout+='L'
        elif opd.type == TokenType.STRING: layout+='S'
    return layout

def _get_reg_value(reg : str):
    if reg == 'R0': return 0
    if reg == 'R1': return 1
    if reg == 'R2': return 2
    if reg == 'R3': return 3
    if reg == 'R4': return 4
    if reg == 'R5': return 5
    if reg == 'R6': return 6
    if reg == 'R7': return 7

def _get_value(opd, stmt, sym_table):
    if opd.type == TokenType.REGISTER: return _get_reg_value(opd.value)
    if opd.type == TokenType.NUMBER:   return int(opd.value[1:]) if not 'x' in opd.value else int(opd.value,16) if opd.value[0:2] == '0x' else int(('0'+opd.value),16)
    if opd.type == TokenType.IDENT:    return (int(sym_table[opd.value],16) - (int(stmt.address,16)+1))   

class Encoder():
    def encode(self, stmts, sym_table):
        words = []

        for stmt in stmts:
            if stmt.op == None: continue
            if stmt.op == '.END': break
            if stmt.op == '.ORIG': words.append('0'+stmt.operands[0].value); continue
            if stmt.op == '.BLKW':
                value=stmt.operands[0].value
                n = int(('0' + value),16) if 'x' in value else int(value[1:]) 
                for i in range(n): words.append('0x0000')
                continue
            if stmt.op == '.STRINGZ':
                for c in stmt.operands[0].value[1:-1]:
                    ch=f'0x{ord(c):04X}'
                    words.append(ch)
                words.append('0x0000')
                continue
            if stmt.op == '.FILL':
                value=stmt.operands[0].value
                if stmt.operands[0].type != TokenType.NUMBER:
                    words.append(sym_table[value])
                else:
                    num=('0' + value) if 'x' in value else f"0x{(int(value[1:]) & 0xFFFF):04X}"
                    words.append(num)
                continue
            word = 0
            ops=stmt.op
            if len(stmt.op) > 2 and stmt.op[0:2] == 'BR':
                ops=stmt.op[0:2]
                if 'P' in stmt.op: word|=(1 << 9)
                if 'Z' in stmt.op: word|=(1 << 10)
                if 'N' in stmt.op: word|=(1 << 11)
            elif stmt.op == 'BR':
                word|=(1 << 9)|(1 << 10)|(1 << 11)

            base, fields = LAYOUTS[(ops,_get_layout(stmt.operands))]
            for opd, (shift, bits) in zip(stmt.operands,fields):
                # print(f'Operand: {opd}, Shift: {shift}, Bits: {bits}')
                value=_get_value(opd,stmt,sym_table)
                word|=(value & ((1 << bits) - 1)) << shift
            # print(f'OPCODE: {stmt.op:<5} -> | {(base|word):016b} | 0x{(base|word):04X}\n')
            words.append(f"0x{(base|word):04X}")
        return words
