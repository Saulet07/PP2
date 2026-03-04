x = int(input())
arr = list(map(int, input().split()))
k = all(i >= 0 for i in arr)
if k:
    print("Yes")
else:
    print("No")