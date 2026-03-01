import re

s = input()

dates = re.findall("\d{2}/\d{2}/\d{4}", s)
print(len(dates))