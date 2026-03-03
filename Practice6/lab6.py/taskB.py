x = int(input())
arr = map(int, input().split())

nums = list(filter(lambda s: s % 2 == 0, arr))
print(len(nums))