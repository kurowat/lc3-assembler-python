import struct

def write_sym_table(file, sym_table):
    with open(file, 'w') as f:
        for label in sym_table:
            f.write(f'{sym_table[label]} {label}\n')

def write_bytes(file, insts):
    with open(file, 'wb') as f:
        for inst in insts:
            f.write(struct.pack('>H', int(inst, 16)))

def get_bytes(insts):
    b = []
    for inst in insts:
        b.append(struct.pack('>H', int(inst, 16)))
    return b
