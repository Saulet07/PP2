import re
s = input()
k = re.findall(r"\b\w{3}\b", s)
print(len(k))