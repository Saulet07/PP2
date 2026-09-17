a = list(map(int, input().split()))
b = list(map(int, input().split()))
a.pop(0)
b.pop(0)
c = a + b
c.sort()
print(*c)