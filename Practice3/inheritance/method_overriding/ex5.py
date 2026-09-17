class exersize:
    def __init__(self, x):
        self.x = x
        self.y = 19
        self.g = x + self.y

n = int(input())
a = exersize(n)
print(a)