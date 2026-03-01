import re
s = input()
pattern = re.compile("^\d+$")
k = pattern.findall(s)
if k:
    print("Match")
else:
    print("No match")
