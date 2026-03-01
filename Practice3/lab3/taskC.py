s = input()

words = {
    "ZER": "0",
    "ONE": "1",
    "TWO": "2",
    "THR": "3",
    "FOU": "4",
    "FIV": "5",
    "SIX": "6",
    "SEV": "7",
    "EIG": "8",
    "NIN": "9"
}
op = ""
if "+" in s:
    op = "+"
elif "-" in s:
    op = "-"
else:
    op = "*"

a, b = s.split(op)

def number(x):
    num = ""
    for i in range(0, len(x), 3):
        part = x[i:i+3]
        num += words[part]
    return int(num)

num1 = number(a)
num2 = number(b)

result = ""
if op == "+":
    result = num1 + num2
elif op == "-":
    result = num1 - num2
else:
    result = num1 * num2

answer = ""
for digit in str(result):
    if digit == "0":
        answer += "ZER"
    elif digit == "1":
        answer += "ONE"
    elif digit == "2":
        answer += "TWO"
    elif digit == "3":
        answer += "THR"
    elif digit == "4":
        answer += "FOU"
    elif digit == "5":
        answer += "FIV"
    elif digit == "6":
        answer += "SIX"
    elif digit == "7":
        answer += "SEV"
    elif digit == "8":
        answer += "EIG"
    elif digit == "9":
        answer += "NIN"

print(answer)