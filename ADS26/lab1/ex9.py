t = int(input())

for _ in range(t):
    n = int(input())

    deck = list(range(1, n + 1))
    ans = [0] * n

    for i in range(1, n + 1):
        r = i % len(deck)

        for j in range(r):
            x = deck.pop(0)
            deck.append(x)

        card = deck.pop(0)
        ans[card - 1] = i

    print(*ans)