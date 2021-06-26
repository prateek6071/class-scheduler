import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

setup(
    name = "Yottabit1's Scheduler",
    version = "1.0.0",
    description = "A scheduling application",
    executables = [Executable(script = "InitApp.py", base = None)])