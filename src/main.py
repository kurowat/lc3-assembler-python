from lexer import Lexer
from parser import Parser
import itertools

source = 'tests/label_test.asm'
lexer = Lexer()
parser = Parser()

tokens = lexer.tokenize(source)
statements = parser.parse(tokens)

# source -> lexer -> parser     -> encoder -> write_out
#                 -> sym_table  
