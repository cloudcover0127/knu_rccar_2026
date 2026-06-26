import sys


print(sys._frame().f_code)
print(sys._frame().f_locals)
print(sys._frame().f_globals)