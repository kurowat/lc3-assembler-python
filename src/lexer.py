from common import OPCODES, TokenType, Token

DIRECTIVE=TokenType.DIRECTIVE
STRING=TokenType.STRING
COMMA=TokenType.COMMA
NUMBER=TokenType.NUMBER
REGISTER=TokenType.REGISTER
OPCODE=TokenType.OPCODE
IDENT=TokenType.IDENT

def _tokenize_line(line: str, line_no: int):
    token_list = []
    n = len(line)
    i = 0
    while i < n:
        c = line[i]
        if c == ';':
            break
        if c in ' ,\t':
            i+=1
        # if c == ',':
        #     token_list.append(Token(COMMA,',',line_no))
        #     i+=1
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
            token_list.append(Token(NUMBER,line[beg:i],line_no))
            continue

        if c == '"':
            beg=i
            i+=1
            while i < n and line[i] != '"': i+=1
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
    return token_list

class Lexer():
    def tokenize(self, source : str):
        tokens = []
        line_no = 1
        with open(source, 'r') as file:
            for line in file:
                tokens.append(_tokenize_line(line.strip(),line_no))
                line_no+=1
        return list(filter(None,tokens))


