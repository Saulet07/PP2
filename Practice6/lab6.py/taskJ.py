x = int(input())
arr = list(map(int, input().split()))
result = sum(map(bool, arr))
print(result)