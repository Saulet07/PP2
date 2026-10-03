n, k = map(int, input().split())
a = list(map(int, input().split()))

a.sort()

if k > n:
    print(-1)
else:
    print(a[k - 1])