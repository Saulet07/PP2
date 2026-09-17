a, b = map(int, input().split())
while b != 0:
    temp = a % b
    a = b
    b = temp
print(a)