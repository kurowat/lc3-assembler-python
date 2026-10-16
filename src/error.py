from common import bcolors

class AsmError(Exception):
    def __init__(self, msg, file, line, col, code, length):
        self.msg = msg
        self.file = file
        self.line = line
        self.col = col
        self.code = code
        self.length = length

    def report(self):
        print(f"{bcolors.BOLD}{self.file}:{self.line}:{self.col}{bcolors.ENDC}: {bcolors.FAIL}error:{bcolors.ENDC} {self.msg}")
        left="" if (self.col+self.length) > len(self.code) else self.code[(self.col+self.length):]
        print(f"{self.code[0:self.col]}{bcolors.FAIL}{self.code[self.col:(self.col+self.length)]}{bcolors.ENDC}{left}")
        print(" " * self.col + bcolors.FAIL + "^" * self.length + bcolors.ENDC)
