n = int(input())
a = list(map(int, input().split()))
a = [x ** 2 for x in a]
a.sort()
for i in a:
    print(i, end=" ")