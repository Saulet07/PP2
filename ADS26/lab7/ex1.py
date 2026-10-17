for _ in range(int(input())):
    print(*sorted(input().split(), key=len))