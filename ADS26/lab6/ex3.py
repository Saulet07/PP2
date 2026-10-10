n = int(input())
a = list(map(int, input().split()))
a.sort()
mn = a[1] - a[0]
for i in range(n - 1):
    d = a[i + 1] - a[i]
    if d < mn:
        mn = d
for i in range(n - 1):
    if a[i + 1] - a[i] == mn:
        print(a[i], a[i + 1], end=" ")