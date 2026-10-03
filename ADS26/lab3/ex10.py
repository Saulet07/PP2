# J. The K-th Largest Value
import sys

input = sys.stdin.buffer.readline

n, k = map(int, input().split())

need = []
for _ in range(n):
    x1, y1, x2, y2 = map(int, input().split())
    need.append(max(x2, y2))

need.sort()
print(need[k - 1])

