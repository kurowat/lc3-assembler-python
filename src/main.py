from lexer import Lexer
from parser import Parser
from encoder import Encoder
from symbol_table import build_symbol_table
from common import bcolors
import itertools
import os.path
import sys

if len(sys.argv) != 2:
    print(bcolors.FAIL + 'error: invalid command' + bcolors.ENDC)
    sys.exit(1)

source = sys.argv[1]
if not os.path.isfile(source):
    print(bcolors.FAIL + 'error: file doesn\'t exist' + bcolors.ENDC)
    sys.exit(1)

lexer = Lexer()
parser = Parser()
encoder = Encoder()

tokens = lexer.tokenize(source)
statements = parser.parse(tokens)
sym_table = build_symbol_table(statements)

# for sym in sym_table:
#     print(sym_table[sym], sym)
#
# for stmt in statements:
#     print(stmt)

insts = encoder.encode(statements, sym_table)

print(insts)

# source -> lexer -> parser     -> encoder -> write_out
#                 -> sym_table  
