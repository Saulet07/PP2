import re

s = input()

caps = re.findall("[A-Z]", s)

print(len(caps))