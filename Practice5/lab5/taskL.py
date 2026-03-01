import re
s = input()

k = re.findall("\d{2,}", s)
print(*k)