# K
import sys

input = sys.stdin.buffer.readline

q = int(input())
queries = list(map(int, input().split()))

n, m = map(int, input().split())

pos = {}

for i in range(n):
    row = list(map(int, input().split()))
    for j in range(m):
        pos[row[j]] = (i, j)

for x in queries:
    if x in pos:
        print(pos[x][0], pos[x][1])
    else:
        print(-1)

