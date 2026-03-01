import re
s = input()
x = input()
k = re.split(x, s)
print(*k, sep=",")