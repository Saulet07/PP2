x = int(input())
a = input()
v = []
c = []
for i in range(x):
    if a[i] in 'aeiou':
        v.append(a[i])
    else:
        c.append(a[i])
v.sort()
c.sort()
print("".join(v + c))