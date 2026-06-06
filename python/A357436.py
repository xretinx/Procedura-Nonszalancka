from sympy import isprime
from itertools import islice
def anext(an):
    s = str(an)
    for c in "0123456789":
        for k in range(len(s)+1):
            w = s + c if k == 0 else s[:-k] + c + s[-k:]
            if w[0] != "0" and isprime(int(w)): return int(w)
def agen(an=2):
    while an != None: yield an; an = anext(an)
print(list(islice(agen(), 22)))