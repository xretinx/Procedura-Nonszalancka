from sympy import isprime
from itertools import islice
def anext(an):
    s = str(an)
    for k in range(len(s)+1):
        for c in "0123456789":
            w = s + c if k == 0 else s[:-k] + c + s[-k:]
            if isprime(int(w)): return int(w)
def agen(an=2):
    while an != None: yield an; an = anext(an)
print(list(islice(agen(), 21)))