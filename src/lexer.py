from common import OPCODES, TokenType, Token
from error import AsmError
import sys, os

DIRECTIVE=TokenType.DIRECTIVE
STRING=TokenType.STRING
COMMA=TokenType.COMMA
NUMBER=TokenType.NUMBER
REGISTER=TokenType.REGISTER
OPCODE=TokenType.OPCODE
IDENT=TokenType.IDENT

def _is_hex(val):
    try:
        int('0'+val, 16)
        return True
    except (ValueError, TypeError):
        return False

def _tokenize_line(filename: str, line: str, line_no: int):
    token_list = []
    n = len(line)
    i = 0
    while i < n:
        c = line[i]

        if c == ';':
            break

        if c in ' ,\t':
            i+=1
            continue

        if c == '.':
            beg=i
            i+=1
            while i < n and (line[i].isalnum() or line[i] == '_'):
                i+=1
            token_list.append(Token(DIRECTIVE,line[beg:i],line_no))
            continue

        if c in '#xX':
            beg=i
            i+=1
            while i < n and (line[i].isalnum() or line[i] == '-'):
                i+=1
            if line[beg] == '#' and not line[beg+1:i].lstrip('-').isdigit() or line[beg] == 'x' and not _is_hex(line[beg:i]):
                raise AsmError(f'malformed number',filename,line_no,beg,line,i-beg)

            token_list.append(Token(NUMBER,line[beg:i],line_no))
            continue

        if c == '"':
            beg=i
            i+=1
            while i < n and line[i] != '"': i+=1
            if i == n: raise AsmError(f'unterminated string',filename,line_no,beg,line,i-beg)
            token_list.append(Token(STRING,line[beg:i+1],line_no))
            i+=2
            continue

        if c.isalnum() or c == '_':
            beg=i
            i+=1
            while i < n and (line[i].isalnum() or line[i] == '_'):
                i+=1
            token=line[beg:i].upper()
            if (i - beg) == 2 and token[0] == 'R' and token[1] in '01234567':
                token_list.append(Token(REGISTER,line[beg:i],line_no))
            elif token in OPCODES:
                token_list.append(Token(OPCODE,token,line_no))
            else:
                token_list.append(Token(IDENT,token,line_no))
            continue
        else:
            raise AsmError('invalid character',filename,line_no,i,line,1)

    return token_list

class Lexer():
    def tokenize(self, source : str):
        tokens = []
        line_no = 1
        filename = os.path.basename(source)
        with open(source, 'r') as file:
            for line in file:
                try:
                    tokens.append(_tokenize_line(filename, line.strip(), line_no))
                    line_no+=1
                except AsmError as e:
                    e.report()
                    sys.exit(1)
        return list(filter(None,tokens))
