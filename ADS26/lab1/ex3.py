x = int(input())
prime = True
if 1 >= x:
    prime = False
else:
    for i in range(2, x):
        if x % i == 0:
            prime = False
            break
if prime:
    print("YES")
else:
    print("NO")