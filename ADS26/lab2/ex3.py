n = int(input())
prev = ""
ans = []
for _ in range(n):
    x = input()
    if prev != x:
        ans.append(x)
        prev = x
print(len(ans))
for x in ans:
    print(x)
    


