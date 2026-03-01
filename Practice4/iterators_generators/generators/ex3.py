def even(n):
    for i in range(0, n+1, 2):
        yield i
x = int(input())
even(x)