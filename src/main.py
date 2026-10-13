from lexer import Lexer
from parser import Parser
from symbol_table import build_symbol_table
import itertools

source = 'tests/label_test.asm'
lexer = Lexer()
parser = Parser()

tokens = lexer.tokenize(source)
statements = parser.parse(tokens)

sym_table = build_symbol_table(statements)

for sym in sym_table:
    print(sym_table[sym], sym)

for stmt in statements:
    print(stmt)

# source -> lexer -> parser     -> encoder -> write_out
#                 -> sym_table  
