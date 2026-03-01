import re
s = input()
k = re.search("Name:\s*(.+), \s*Age:\s*(\d+)", s)
print(k.group(1), k.group(2))