from common import SPEC, Operand, TokenType, Statement

REG=Operand.REG
IMM5=Operand.IMM5
IMM6=Operand.IMM6
LABEL=Operand.LABEL 
NUM=Operand.NUM
STR=Operand.STR

# def operand_to_token_type(operand):
#     if operand == IMM5: return TokenType.NUMBER
#     if operand == IMM6: return TokenType.NUMBER
#     if operand == NUM: return TokenType.NUMBER
#     if operand == NUM: return TokenType.NUMBER
#     if operand == STR: return TokenType.STRING
#     if operand == REG: return TokenType.REGISTER

# def check_operands(stmt):

def _get_statement(token: list):
    stmt = Statement()
    stmt.line = token[0].line
    n = len(token)
    i = 0
    while i < n:
        if token[i].type == TokenType.IDENT:
            stmt.label = token[i].value
            i+=1
        if i < n and (token[i].type == TokenType.DIRECTIVE or token[i].type == TokenType.OPCODE):
            stmt.op = token[i].value
            i+=1
            pattern_n = len(SPEC[stmt.op][0])
            while i < n and pattern_n > 0:
                stmt.operands.append(token[i])
                pattern_n-=1
                i+=1
    return stmt


class Parser():
    def parse(self, tokens: list):
        statements = []
        for token in tokens:
            stmt = _get_statement(token)
            statements.append(stmt)
