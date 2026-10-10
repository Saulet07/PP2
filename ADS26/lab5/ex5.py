n, k = map(int, input().split())
sum = 0
for _ in range(n):
    x = input().split()
    y = x[0].strip()
    if y == 'insert':
        sum += int(x[1])
    else:
        print(sum)

