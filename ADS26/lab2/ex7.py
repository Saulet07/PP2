a, b = map(int, input().split())
s = input().split()
b = b % a
v = ""
v1 = ""
for i in range(a):
    if i >= b:
        v += s[i] + " "
    else:
        v1 += s[i] + " "
print(v + v1)