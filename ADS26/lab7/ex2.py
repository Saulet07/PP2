n = int(input())
a = list(map(int, input().split()))
m = int(input())
b = list(map(int, input().split()))
w = a + b 
w.sort()
print(*w)