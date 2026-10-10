n = int(input())
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
        if data < curr.data:
            if curr.left is None:
                curr.left = new
                return root
            curr = curr.left
        else:
            if curr.right is None:
                curr.right = new
                return root
            curr = curr.right
ans = 0
def dfs(root):
    global ans
    if root is None:
        return 0
    left = dfs(root.left)
    right = dfs(root.right)
    ans = max(ans, left + right + 1)
    return max(left, right) + 1
tree = None
lst = list(map(int, input().split()))
for x in lst:
    tree = insert(tree, x)
dfs(tree)
print(ans)