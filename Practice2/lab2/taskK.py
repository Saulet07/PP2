n, l, r = map(int, input().split())
b = list(map(int, input().split()))

for i in range((r - l + 1) // 2):
    b[l + i - 1], b[r - i - 1] = b[r - i - 1], b[l + i - 1]

for i in b:
    print(i, end=" ") 