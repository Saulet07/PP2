import re
s = input().split()
index = ""
for i in range(len(s)):
    if re.search("\S+@\S+\.\S+", s[i]):
        index = s[i]
        break
if index != "":
    print(index)
else:
    print("No email")
