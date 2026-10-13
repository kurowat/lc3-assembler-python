def build_symbol_table(stmts: list):
    LC=None
    n = len(stmts)
    i = 1

    if stmts[0].op == '.ORIG':
        LC=int('0'+stmts[0].operands[0].value,16)

    sym_table = {}
    while i < n:
        stmt = stmts[i]
        if stmt.label != None:
            sym_table[stmt.label] = hex(LC)

        if stmt.op != None:
            word=1
            if stmt.op == '.BLKW':      word=int(stmt.operands[0].value[1:])
            elif stmt.op == '.STRINGZ': word=len(stmt.operands[0].value[1:-1])+1
            LC=LC+word

        stmt.address = hex(LC)
        i+=1
    return sym_table
