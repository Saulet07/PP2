n = int(input())
ans = []
for i in range(n):
    s = input()
    day, month, year = map(int, s.split('-'))
    ans.append((year, month, day, s))
ans.sort()
for x in ans:
    print(x[3])