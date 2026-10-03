n, q = map(int, input().split())
s = list(map(int, input().split()))
for _ in range(q):
    l1, r1, l2, r2 = map(int, input().split())
    sum = 0
    for i in s:
        if l1 <= i <= r1 or l2 <= i <= r2:
            sum += 1
    print(sum)
    
