import re
s = input()
p = input()
r = input()
k = re.sub(p, r, s)
print(k)