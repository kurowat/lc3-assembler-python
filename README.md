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

