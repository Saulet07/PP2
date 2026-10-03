# Submit a solution for A-111284. Mountains
import sys

class TreeNode:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    comms = int(input_data[1])

    root = TreeNode(int(input_data[2]))
    idx = 3

    for _ in range(n - 1):
        data = int(input_data[idx])
        idx += 1
        curr = root
        while True:
            if data <= curr.data:
                if curr.left is None:
                    curr.left = TreeNode(data)
                    break
                curr = curr.left
            else:
                if curr.right is None:
                    curr.right = TreeNode(data)
                    break
                curr = curr.right

    results = []
    for _ in range(comms):
        path = input_data[idx]
        idx += 1
        
        curr = root
        for s in path:
            if curr is None:
                break
            if s == 'L':
                curr = curr.left
            else:
                curr = curr.right

        if curr is None:
            results.append("NO")
        else:
            results.append("YES")

    sys.stdout.write('\n'.join(results) + '\n')

if __name__ == '__main__':
    solve()