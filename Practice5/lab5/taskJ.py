import re
s = input()
k = re.search("cat|dog", s)
if k:
    print("Yes")
else:
    print("No")