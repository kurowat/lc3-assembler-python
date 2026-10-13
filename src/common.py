from dataclasses import dataclass, field
from enum import Enum, auto

class TokenType(Enum):
    DIRECTIVE=auto()
    STRING=auto()
    COMMA=auto()
    NUMBER=auto()
    REGISTER=auto()
    OPCODE=auto()
    IDENT=auto()

class Operand(Enum):
    REG=auto()
    IMM5=auto()
    IMM6=auto()
    LABEL=auto()
    NUM=auto()
    STR=auto()

@dataclass
class Token:
    type  : TokenType
    value : str | int | None
    line  : int

@dataclass
class Statement: 
    label    : str | None = None
    op       : str | None = None
    operands : list = field(default_factory=list)
    line     : int = 0
    address  : int | None = None

REG=Operand.REG
IMM5=Operand.IMM5
IMM6=Operand.IMM6
LABEL=Operand.LABEL 
NUM=Operand.NUM
STR=Operand.STR
SPEC = {
    "ADD"      : [(REG,REG,REG),(REG,REG,IMM5)], 
    "AND"      : [(REG,REG,REG),(REG,REG,IMM5)],
    "BR"       : [(LABEL,)],
    "BRN"      : [(LABEL,)],
    "BRZ"      : [(LABEL,)],
    "BRP"      : [(LABEL,)],
    "BRNZ"     : [(LABEL,)],
    "BRNP"     : [(LABEL,)],
    "BRZP"     : [(LABEL,)],
    "BRNZP"    : [(LABEL,)],
    "JMP"      : [(REG,)],
    "JSR"      : [(LABEL,)],
    "JSRR"     : [(REG,)],
    "LD"       : [(REG,LABEL)],
    "LDI"      : [(REG,LABEL)],
    "LDR"      : [(REG,REG,IMM6)],
    "LEA"      : [(REG,LABEL)],
    "NOT"      : [(REG,REG)],
    "RET"      : [()],
    "RTI"      : [()],
    "ST"       : [(REG,LABEL)],
    "STI"      : [(REG,LABEL)],
    "STR"      : [(REG,REG,IMM6)],
    "GETC"     : [()],
    "OUT"      : [()],
    "PUTS"     : [()],
    "IN"       : [()],
    "PUTSP"    : [()],
    "HALT"     : [()],
    "TRAP"     : [(NUM,)],
    ".ORIG"    : [(NUM,)],
    ".FILL"    : [(NUM,),(LABEL,)],
    ".BLKW"    : [(NUM,)],
    ".STRINGZ" : [(STR,)],
    ".END"     : [()],
}

DIRECTIVES = {
    ".ORIG",
    ".FILL",
    ".BLKW",
    ".STRINGZ",
    ".END",
}

OPCODES = {
    "ADD",
    "AND",
    "NOT",
    "LD",
    "LDI",
    "LDR",
    "LEA",
    "ST",
    "STI",
    "STR",
    "BR",
    "BRN",
    "BRZ",
    "BRP",
    "BRNZ",
    "BRNP",
    "BRZP",
    "BRNZP",
    "JMP",
    "JSR",
    "JSRR",
    "RET",
    "RTI",
    "TRAP",
    "HALT",
    "GETC",
    "OUT",
    "PUTS",
    "IN",
    "PUTSP",
}
