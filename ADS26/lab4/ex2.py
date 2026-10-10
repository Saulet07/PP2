class Treenode:
    def __init__(self, data):
        self.data = data 
        self.left = None 
        self.right = None 
def insert(root, data):
    new = Treenode(data)
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
def getsize(root):
    if root is None:
        return 0
    return 1 + getsize(root.left) + getsize(root.right)



n = int(input())
tree = None 
for i in map(int, input().split()):
    tree = insert(tree, i)
x = int(input())
curr = tree
while curr.data != x:
    if x > curr.data:
        curr = curr.right 
    elif x < curr.data:
        curr = curr.left 
print(getsize(curr))