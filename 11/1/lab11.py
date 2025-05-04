# Evelyn
# CPS 196

def line(a, b='!'):
    return a * b + "\n"

def mixedLine(a, b, c, d):
    return a * b + c * d + "\n"

def rectangle(a, b, c='*'):
    return ''.join([line(b, c) for _ in range(a)])

def triangle(a, b='$'):
    return ''.join([line(i, b) for i in range(1, a + 1)])