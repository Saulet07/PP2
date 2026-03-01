import re
s = input()
k = re.findall("\w+", s)
print(len(k))