import re
s = input()
k = re.findall("\d+", s)
print(*k)