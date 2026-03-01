import re

text = open("Practice5/receipt_parser/raw.txt").read()
print(re.findall(r"\d+", text))