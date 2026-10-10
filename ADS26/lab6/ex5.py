n, m = map(int, input().split())
a = []
for _ in range(n):
    l = list(map(int, input().split()))
    a.append(l)
for j in range(m):
    b = []
    for i in range(n):
        b.append(a[i][j])
    b.sort(reverse=True)
    for i in range(n):
        a[i][j] == b[i]
for i in range(n):
    print(*a[i])