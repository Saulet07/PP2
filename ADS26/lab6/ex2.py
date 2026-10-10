n, m = map(int, input().split())
a = list(map(int, input().split())) if n > 0 else []
b = list(map(int, input().split())) if m > 0 else []
a.sort()
b.sort()
ans = []
i = 0
j = 0
while i < n and j < m:
    if a[i] == b[j]:
        ans.append(a[i])
        i += 1
        j += 1
    elif a[i] < b[j]:
        i += 1
    else:
        j += 1
print(*ans)