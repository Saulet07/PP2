T = int(input())
for _ in range(T):
    N = int(input())
    s = input().split()
    count = {}
    q = []
    ans = []
    for x in s:
        if x not in count:
            count[x] = 0
        count[x] += 1
        q.append(x)
        while q and count[q[0]] > 1:
            q.pop(0)
        if q:
            ans.append(q[0])
        else:
            ans.append("-1")
    print(*ans)
    
    