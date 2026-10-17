from common import SPEC, Operand, TokenType, Statement, ErrorCtx, DIRECTIVES, OPCODES
from lexer import Lexer
from error import AsmError
import sys

REG=Operand.REG
IMM5=Operand.IMM5
IMM6=Operand.IMM6
LABEL=Operand.LABEL 
NUM=Operand.NUM
STR=Operand.STR

DIRECTIVE=TokenType.DIRECTIVE
STRING=TokenType.STRING
NUMBER=TokenType.NUMBER
REGISTER=TokenType.REGISTER
OPCODE=TokenType.OPCODE
IDENT=TokenType.IDENT

def _opd_to_ttype(opd):
    if opd == IMM5:  return NUMBER
    if opd == IMM6:  return NUMBER
    if opd == NUM:   return NUMBER
    if opd == NUM:   return NUMBER
    if opd == STR:   return STRING
    if opd == REG:   return REGISTER
    if opd == LABEL: return IDENT

def _get_ttype(tokens, start, end):
    ttype = []
    for i in range(start, end):
        ttype.append(tokens[i].type)
    return ttype

class Parser():
    def __init__(self, lexer):
        self.lexer = lexer

    def get_statement(self, tokens):
        stmt = Statement()
        err = None
        n = len(tokens)
        i = 0

        if tokens[0].type == IDENT:
            stmt.label = tokens[0].value
            i += 1
        elif tokens[0].type in (REG,STRING,NUMBER):
            err = ErrorCtx('unknown opcode', tokens[0].value, len(tokens[0].value), tokens[0].line)
            return (1, stmt, err)

        val = 0
        if i < n:
            if tokens[i].type in (OPCODE, DIRECTIVE) and (tokens[i].value in DIRECTIVES or tokens[i].value in OPCODES):
                stmt.op = tokens[i].value
                i += 1
            else:
                err = ErrorCtx('unknown opcode or directive', None, 0, tokens[i].line)
                return (1, stmt, err)


            if (len(tokens) - i) != len(SPEC[stmt.op][0]):
                err = ErrorCtx('wrong operand count', None, 0, tokens[0].line)
                return (1, stmt, err)

            val = 1
            for patt in SPEC[stmt.op]:
                patt_ttype = [_opd_to_ttype(x) for x in patt]
                tk_ttype = _get_ttype(tokens, i, n)
                print(patt_ttype, tk_ttype)

                if not all(x == y for x, y in zip(patt_ttype, tk_ttype)):
                    continue
                while i < n:
                    stmt.operands.append(tokens[i])
                    i += 1
                val = 0

            if val == 1: err = ErrorCtx('wrong operand type or invalid register', None, 0, tokens[0].line)

        return (val, stmt, err)

    def parse(self):
        stmts = []
        lines = []

        while True:
            try:
                empty, line, tokens = self.lexer.tokenize_line()
                lines.append(line)
                if empty == 1: break
                if len(tokens) != 0:
                    status, stmt, err = self.get_statement(tokens)
                    if status == 1:
                        col = line.find(err.token) if err.token != None else 0
                        token_len = err.token_len if err.token_len != 0 else len(line)
                        raise AsmError(err.msg,self.lexer.filename,err.line,col,line,token_len)

                    stmt.line = self.lexer.line_no
                    stmts.append(stmt)
                    if stmt.op == '.END': break;
            except AsmError as e:
                e.report()
                sys.exit(1)

        for stmt in stmts:
            print(stmt)

        try:
            n = len(stmts)
            if n > 0:
                if stmts[0].op != '.ORIG':
                    raise AsmError('Missing .ORIG',self.lexer.filename,stmts[0].line,0,lines[stmts[0].line-1], len(lines[stmts[0].line-1]))
                if stmts[n-1].op != '.END':
                    raise AsmError('Missing .END',self.lexer.filename,stmts[n-1].line,0,lines[stmts[n-1].line-1], len(lines[stmts[n-1].line-1]))

        except AsmError as e:
            e.report()
            sys.exit(1)

        return stmts
