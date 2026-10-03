a = []

while 1:
    t = input().split()
    c = int(t[0])

    if c == 0: break
    if c == 1:
        a.insert(int(t[2]), int(t[1]))
    elif c == 2:
        a.pop(int(t[1]))
    elif c == 3:
        print(*a) if a else print(-1)
    elif c == 4:
        p, q = int(t[1]), int(t[2])
        a.insert(q, a.pop(p))
    elif c == 5:
        a.reverse()
    elif c == 6:
        x = int(t[1]) % len(a)
        a[:] = a[x:] + a[:x]
    elif c == 7:
        x = int(t[1]) % len(a)
        a[:] = a[-x:] + a[:-x]