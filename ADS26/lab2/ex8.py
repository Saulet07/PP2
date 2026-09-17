n = int(input())
s = list(map(int, input().split()))
sum = []
for i in range(1, n + 1):
    for j in range(n - i + 1):
        b = 0
        for x in range(j, j + i):
            b += s[x]
        sum.append(b)    
        b = 0
m = -100000
for i in range(len(sum)):
    if sum[i] > m:
        m = sum[i]
print(m)
