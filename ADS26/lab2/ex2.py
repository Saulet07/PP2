n = int(input())
s = list(map(int, input().split()))

print(*s[::2])