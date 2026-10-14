from lexer import Lexer
from parser import Parser
from encoder import Encoder
from symbol_table import build_symbol_table
from common import bcolors
import struct
import itertools
import os.path
import sys

if len(sys.argv) != 2:
    print(bcolors.FAIL + 'fetal error: ' + bcolors.ENDC + 'missing required argument <file>')
    print('Usage: lc3-asm <file>')
    sys.exit(1)

source = sys.argv[1]
if not os.path.isfile(source):
    print(bcolors.FAIL + 'fetal error: ' + bcolors.ENDC + f'file \'{source}\' does not exist')
    sys.exit(1)

lexer = Lexer()
parser = Parser()
encoder = Encoder()

tokens = lexer.tokenize(source)
statements = parser.parse(tokens)
sym_table = build_symbol_table(statements)
insts = encoder.encode(statements, sym_table)

filename = os.path.splitext(os.path.basename(source))[0]
out_sym = filename + '.sym'
out_obj = filename + '.obj'

if len(sym_table) > 0:
    with open(out_sym, 'w') as f:
        for label in sym_table:
            f.write(f'{sym_table[label]} {label}\n')

with open(out_obj, 'wb') as f:
    for inst in insts:
        f.write(struct.pack('>H', int(inst, 16)))
