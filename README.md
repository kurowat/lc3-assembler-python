## Build
```bash
git clone https://github.com/kurowat/lc3-assembler-python.git
cd lc3-assembler-python/
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python build.py
```

## Usage
```
lc3-asm <file>
```
**Note:** executable is located in dist/ after build

## Simulation
After you compiled the assembly file, you'll get two files:
- xxx.obj: binary file.
- xxx.sym: symbol table file.

You can run the simulation on website: [LC-3 Simulator](https://wchargin.com/lc3web/)

## Error cases

| ERROR | Example |
| --- | --- |
| Invalid character | $#@ etc. |
| Malformed number | x3G / #2f |
| Unterminated string in .STRINGZ | .STRINGZ "abc |
| Wrong operand count | NOT R1, R2, R3 |
| Wrong operand type | `ADD R1, 2, R3 |
| Missing .ORIG | NOT R1, R2<br>.END |
| Missing .END | .ORIG x3000<br>ADD R1,R1,R2<br> |
