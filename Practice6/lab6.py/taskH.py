x = int(input())
arr = list(map(int, input().split()))
k = set()
for i in arr:
    k.add(i)
for i in sorted(k):
    print(i, end=" ")