n = int(input())
s = list(map(int, input().split()))
a = len(s) // 2
for i in range(len(s)):
    if i != a:
        print(s[i], end=" ")
