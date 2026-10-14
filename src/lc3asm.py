from lexer import Lexer
from parser import Parser
from encoder import Encoder
from symbol_table import build_symbol_table

def assemble(source : str):
    lexer = Lexer()
    parser = Parser()
    encoder = Encoder()

    tokens = lexer.tokenize(source)
    statements = parser.parse(tokens)
    sym_table = build_symbol_table(statements)
    insts = encoder.encode(statements, sym_table)

    return insts, sym_table
