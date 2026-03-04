x = int(input())
arr1 = list(map(int, input().split()))
arr2 = list(map(int, input().split()))
k = 0
for i, y in zip(arr1, arr2):
    k += i * y
print(k)