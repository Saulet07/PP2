# Submit a solution for A-111284. Mountains
class TreeNode:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None
def insert(root, data):
    new = TreeNode(data)
    if root is None:
        return new
    curr = root
    while True:
        if data <= curr.data:
            if curr.left is None:
                curr.left = new
                return root
            curr = curr.left
        else:
            if curr.right is None:
                curr.right = new
                return root
            curr = curr.right
n, q = map(int, input().split())
a = list(map(int, input().split()))
tree = None
for x in a:
    tree = insert(tree, x)
for i in range(q):
    path = input()
    curr = tree
    for s in path:
        if s == 'L':
            curr = curr.left
        else:
            curr = curr.right
        if curr is None:
            break
    if curr is None:
        print("NO")
    else:
        print("YES")