n = int(input())
a = input().split()
p = input()
for i in range(n):
    if a[i] > p:
        print(a[i])
        break
else:
    print(a[0])