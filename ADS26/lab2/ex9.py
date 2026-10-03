from collections import deque

a = deque()

while 1:
    x = input().split()
    c = x[0]

    if c == 'add_front':
        a.appendleft(x[1])
        print('ok')
    elif c == 'add_back':
        a.append(x[1])
        print('ok')
    elif c == 'erase_front':
        print(a.popleft() if a else 'error')
    elif c == 'erase_back':
        print(a.pop() if a else 'error')
    elif c == 'front':
        print(a[0] if a else 'error')
    elif c == 'back':
        print(a[-1] if a else 'error')
    elif c == 'clear':
        a.clear()
        print('ok')
    else:
        print('goodbye')
        break