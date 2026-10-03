# Problem D Win me if you can!
import sys
from bisect import bisect_right

d = list(map(int, sys.stdin.buffer.read().split()))

n = d[0]
a = sorted(d[1:n+1])
q = d[n+1]

s = [0] * (n + 1)
for i in range(n):
    s[i+1] = s[i] + a[i]

ans = []
for x in d[n+2:]:
    k = bisect_right(a, x)
    ans.append(f"{k} {s[k]}")

sys.stdout.write("\n".join(ans))