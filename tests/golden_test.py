from pathlib import Path
import sys, os, struct, pytest
sys.path.insert(1, os.path.join("/".join(os.path.realpath(__file__).split("/")[0:-2]),"src"))
from lc3asm import assemble
from helper import get_bytes

GOLDEN=Path(__file__).parent / "golden"
CASES = sorted(p for p in GOLDEN.iterdir() if p.is_dir())

def assert_words_equal(got, exp):
    g = struct.unpack(f">{len(got)//2}H", got)
    e = struct.unpack(f">{len(exp)//2}H", exp)
    for i in range(max(len(g), len(e))):
        gi = g[i] if i < len(g) else None
        ei = e[i] if i < len(e) else None
        assert gi == ei, f"word {i}: expected {ei}, got {gi}"

@pytest.mark.parametrize("case", CASES, ids=lambda p: p.name)
def test_golden(case):
    asm_path=case /  f'{case.name}.asm'
    insts, sym_table = assemble(asm_path)
    data = get_bytes(insts)

    obj_path=case /  f'{case.name}.obj'
    sym_path=case /  f'{case.name}.sym'
    sym_txt="".join(f'{a} {n}\n' for n, a in sym_table.items())

    assert_words_equal(b"".join(data), obj_path.read_bytes())
    if os.path.isfile(sym_path):
        assert sym_txt == sym_path.read_text()
