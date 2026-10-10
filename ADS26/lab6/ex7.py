n = int(input())
users = {}
for _ in range(n):
    old, new = input().split()
    if old in users:
        users[new] = users[old]
        del users[old]
    else:
        users[new] = old 
ans = []
for x in users:
    y = users[x]
    ans.append((y, x))
ans.sort()
print(len(ans))
for x, y in ans:
    print(x, y)