# H. Subarray with Sum at Least K
import sys
from bisect import bisect_left

input = sys.stdin.buffer.readline

n, k = map(int, input().split())
a = list(map(int, input().split()))

prefix = [0] * (n + 1)

for i in range(n):
    prefix[i + 1] = prefix[i] + a[i]

answer = n

for i in range(n):
    need = prefix[i] + k
    j = bisect_left(prefix, need, i + 1)

    if j <= n:
        answer = min(answer, j - i)

print(answer)