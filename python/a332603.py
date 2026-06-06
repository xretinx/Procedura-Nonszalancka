from itertools import islice
def issquarefree(s):
    for l in range(1, len(s)//2 + 1):
        for i in range(len(s)-2*l+1):
            if s[i:i+l] == s[i+l:i+2*l]: return False
    return True
def nexts(s):
    for k in range(len(s)+1):
        for c in "123":
            w = s + c if k == 0 else s[:-k] + c + s[-k:]
            if issquarefree(w): return w
def agen(s="1"):
    while s != None: yield int(s); s = nexts(s)
print(list(islice(agen(), 21)))