import re
s = input()
x = input()
r = re.findall(re.escape(x), s)
print(len(r))