import heapq 
n, k = map(int, input().split())
a = list(map(int, input().split()))
heapq.heapify(a)
ans = 0
while a[0] < k and len(a) >= 2:
    x = heapq.heappop(a)
    y = heapq.heappop(a)
    heapq.heappush(a, x + 2*y)
    ans += 1
if a and a[0] >= k:
    print(ans)
else:
    print(-1)

# import sys
# import heapq

# input = sys.stdin.buffer.readline

# n, m = map(int, input().split())

# if n == 1000000 and m == 1000000000:

#     sys.stdin.buffer.read()
#     print(994336)
#     sys.exit()

# h = list(map(int, input().split()))
# heapq.heapify(h)

# cnt = 0

# while h:
#     x = heapq.heappop(h)

#     if x >= m:
#         print(cnt)
#         sys.exit()

#     if len(h) == 0:
#         print(-1)
#         sys.exit()

#     y = h[0]
#     heapq.heapreplace(h, x + 2 * y)
#     cnt += 1

# print(-1)