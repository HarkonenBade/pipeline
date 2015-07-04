import math
from pipeline import Pipeline as PL

@PL.register
def ints(_):
    cur = 0
    while True:
        yield cur
        cur += 1

def to_string(elm):
    out = ""
    tmp = elm
    while tmp >= 0:
        out += chr(ord('a') + tmp % 26)
        tmp = int(math.floor(tmp/26) - 1)
    return out[::-1]

@PL.register
def print_out(lst):
    for elm in lst:
        print elm

PL().ints().map(to_string).take(30).print_out()
