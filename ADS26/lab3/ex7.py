# G
import math

n, k = map(int, input().split())
a = list(map(int, input().split()))

left = 0.0
right = max(a)

for _ in range(60):
    mid = (left + right) / 2

    pieces = sum(math.floor(x / mid) for x in a)

    if pieces >= k:
        left = mid
    else:
        right = mid

print(f"{left:.9f}")