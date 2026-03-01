import re
s = input()
a = input()
text = re.search(a, s)
if text:
    print("Yes")
else:
    print("No")