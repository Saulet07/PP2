import heapq

n = int(input())
a = list(map(int, input().split()))

# Үлкен сандарды бірінші алу үшін минус қоямыз
a = [-x for x in a]

heapq.heapify(a)

while len(a) > 1:

    # Ең үлкен екі тасты аламыз
    x = -heapq.heappop(a)
    y = -heapq.heappop(a)

    # Егер салмақтары әртүрлі болса
    if x != y:
        new = x - y
        heapq.heappush(a, -new)

if a:
    print(-a[0])
else:
    print(0)