arr = list(map(int, input().split()))
k = len(arr)
odd = True
for i in range(k):
    if arr[i] % 2 == 1:
        odd = False
if odd:
    print("0")
else:
    print("1")