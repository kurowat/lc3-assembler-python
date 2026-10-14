from common import bcolors
from lc3asm import assemble
from helper import write_sym_table, write_bytes
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

insts, sym_table = assemble(source)
filename = os.path.splitext(os.path.basename(source))[0]
out_sym = filename + '.sym'
out_obj = filename + '.obj'

if len(sym_table) > 0: write_sym_table(out_sym, sym_table)
write_bytes(out_obj, insts)
