x = int(input())
arr1 = input().split()
arr2 = input().split()
find = input()
found = -1000000
k = True
for i, j in zip(arr1, arr2):
    if find == i:
        found = j
if found == -1000000:
    print("Not found")
else:
    print(found)