# Problem C. Debugging
from bisect import bisect_left

n, m = map(int, input().split())
a = list(map(int, input().split()))

p = []
s = 0
for x in a:
    s += x
    p.append(s)

for _ in range(m):
    print(bisect_left(p, int(input())) + 1)