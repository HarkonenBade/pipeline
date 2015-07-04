import math
from pipeline import Pipeline as PL

@PL.register
def ints(_):
    a = 0
    while True:
        yield a
        a += 1

def to_string(i):
    out = ""
    tmp = i
    while tmp >= 0:
        out += chr(ord('a') + tmp % 26)
        tmp = math.floor(tmp/26) - 1
    return out[::-1]

print(list(PL().ints().map(to_string).take(30)))
        
