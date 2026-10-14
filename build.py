import PyInstaller.__main__
import os

PyInstaller.__main__.run([
    "src/main.py",
    "--onefile",
    "--name=lc3-asm",
    "--clean",
])
