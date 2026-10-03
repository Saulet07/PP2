#  F Robin Hood stealing the Gold
n, h = map(int, input().split())
a = list(map(int, input().split()))
left = 1
right = max(a)
while left < right:
    k = (left + right) // 2
    hours = 0
    for x in a:
        hours += (x + k - 1) // k
    if hours <= h:
        right = k
    else:
        left = k + 1
print(left)
