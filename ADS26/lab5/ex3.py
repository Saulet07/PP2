# Submit a solution for C-Standard problem about soccer
import heapq
n, m = map(int, input().split())
a = list(map(int, input().split()))
a = [-x for x in a]
heapq.heapify(a)
ans = 0
for i in range(m):
    x = -heapq.heappop(a)
    ans += x 
    if x > 1:
        heapq.heappush(a, -(x - 1))
print(ans)