import heapq
n, k = map(int, input().split())
h = []
total = 0
for _ in range(n):
    command = input().split()
    if command[0] == "insert":
        x = int(command[1])
        heapq.heappush(h, x)
        total += x
        if len(h) > k:
            total -= heapq.heappop(h)
    else:
        print(total)