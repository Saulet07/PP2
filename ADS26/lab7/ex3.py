n = int(input())
a = list(map(int, input().split()))

def merge(a):
    if len(a) <= 1:
        return a, 0
    m = len(a) // 2
    l, x = merge(a[:m])
    r, y = merge(a[m:])
    b = []
    i = j = 0
    count = x + y
    while i < len(l) and j < len(r):
        if l[i] <= r[j]:
            b.append(l[i])
            i += 1
        else:
            b.append(r[j])
            count += len(l) - i
            j += 1
    return b + l[i:] + r[j:], count
print(merge(a)[1])