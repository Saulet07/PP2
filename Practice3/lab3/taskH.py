class Account:
    def __init__(self, B, W):
        self.B = B
        self.W = W
    def show(self):
        if self.B > self.W:
            return "Insufficient Funds"
        else:
            return self.W -self.B
B, W = map(int, input().split())
p1 = Account(W, B)
print(p1.show())