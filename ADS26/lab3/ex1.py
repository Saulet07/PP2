n = int(input())
s = list(map(int, input().split()))
x = int(input())
t = False
for i in range(n):
    if s[i] == x:
        t = True
        break
    else:
        t = False
if t:
    print("YES")
else:   
    print("NO")