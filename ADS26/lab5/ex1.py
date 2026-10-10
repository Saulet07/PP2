# Submit a solution for A-Optimizing Program
import heapq
n = int(input())
a = list(map(int, input().split()))
heapq.heapify(a)
ans = 0
while len(a) > 1:
    x = heapq.heappop(a)
    y = heapq.heappop(a)
    s = x + y
    ans += s
    heapq.heappush(a, s)
print(ans)