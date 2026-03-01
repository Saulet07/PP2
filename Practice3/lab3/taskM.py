arr = list(map(int, input().split()))
res = []
for x in arr:
    prime = True
    if x > 1:
        for i in range(2, x):
            if x % i == 0:
                prime = False
                break
        if prime:
            res.append(x)

if res:
    for i in res:
        print(i, end=" ")
else:
    print("No primes")


