n, m = map(int, input().split())
a = []

for i in range(n):
    a.append(list(map(int, input().split())))

a.sort(key=lambda x: (-sum(x), x))

for row in a:
    print(*row)