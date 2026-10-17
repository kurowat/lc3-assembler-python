from common import OPCODES, TokenType, Token
from error import AsmError
import sys, os

DIRECTIVE=TokenType.DIRECTIVE
STRING=TokenType.STRING
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

class Lexer():
    def __init__(self, source: str):
        self.source = source
        self.line_no = 0
        self.filename = os.path.basename(source)

        try:
            self.ctx = open(source, 'r')
        except FileNotFoundError:
            print(f"fatal error: file '{source}' not found")

    def __del__(self):
        self.ctx.close()

    def tokenize_line(self):
        self.line_no += 1
        line = self.ctx.readline()
        empty = 0 if len(line) > 0 else 1
        line = line.strip()
        tokens = []

        n = len(line)
        i = 0
        while i < n:
            c = line[i]

            if c == ';': break

            if c in ' ,\t': i+=1; continue

            if c == '.':
                beg=i
                i+=1
                while i < n and (line[i].isalnum() or line[i] == '_'): i+=1
                tokens.append(Token(DIRECTIVE,line[beg:i],self.line_no))
                continue

            if c in '#xX':
                beg=i
                i+=1
                while i < n and (line[i].isalnum() or line[i] == '-'): i+=1
                if line[beg] == '#' and not line[beg+1:i].lstrip('-').isdigit() or line[beg] == 'x' and not _is_hex(line[beg:i]):
                    raise AsmError(f'malformed number',self.filename,self.line_no,beg,line,i-beg)
                tokens.append(Token(NUMBER,line[beg:i],self.line_no))
                continue

            if c == '"':
                beg=i
                i+=1
                while i < n and line[i] != '"': i+=1
                if i == n: raise AsmError(f'unterminated string',self.filename,self.line_no,beg,line,i-beg)
                tokens.append(Token(STRING,line[beg:i+1],self.line_no))
                i+=2
                continue

            if c.isalnum() or c == '_':
                beg=i
                i+=1
                while i < n and (line[i].isalnum() or line[i] == '_'): i+=1
                token=line[beg:i].upper()
                if (i - beg) == 2 and token[0] == 'R' and token[1] in '01234567':
                    tokens.append(Token(REGISTER,line[beg:i],self.line_no))
                elif token in OPCODES:
                    tokens.append(Token(OPCODE,token,self.line_no))
                else:
                    tokens.append(Token(IDENT,token,self.line_no))
                continue
            else:
                raise AsmError('invalid character',self.filename,self.line_no,i,line,1)

        return empty, line, tokens
