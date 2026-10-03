# Submit a solution for H-111743. Greater Sum Tree
n = int(input())
a = list(map(int, input().split()))
sum = 0 
ans = []
a.sort()
for i in range(n - 1, -1 ,-1):
    sum += a[i]
    ans.append(sum)
print(*ans)