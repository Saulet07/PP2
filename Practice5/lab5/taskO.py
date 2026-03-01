import re
s = input()
def f(s):
    k = s.group()
    return k + k
print(re.sub("\d", f, s))
