import random
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
        self.father = None
        self.left_count = 0
        self.right_count = 0
        self.counts = 1
class BST:
    def __init__(self, x=None):
        self.root = TreeNode(x) if x else None

    def search(self, x):
        node = self.root
        if not node:
            return node
        while True:
            if node.val == x:
                return node
            if x > node.val:
                if not node.right:
                    return node
                node = node.right
            else:
                if not node.left:
                    return node
                node = node.left
    def update(self, node, k):
        while node.father:
            if node.father.left is node:
                node.father.left_count += k
            else:
                node.father.right_count += k
            node = node.father
    def insert(self, x):
        if not self.root:
            self.root = TreeNode(x)
            return
        root = self.search(x)
        if root.val == x:
            root.counts += 1
            self.update(root, 1)
        elif root.val > x:
            root.left = TreeNode(x)
            root.left.father = root
            self.update(root.left, 1)
        else:
            root.right = TreeNode(x)
            root.right.father = root
            self.update(root.right, 1)

    def successor(self, node):
        node = node.right
        while node.left:
            node = node.left
        return node
    def remove(self, x):
        node = self.search(x)
        if not node:
            return
        if node.counts != 1:
            node.counts -= 1
            self.update(node, -1)
            return 'no'
        if not node.left:
            if not node.father:
                self.root = node.right
                if self.root:
                    self.root.father = None
                return
            else:
                if node.father.val > node.val:
                    node.father.left = node.right
                    node.father.left_count -= 1
                else:
                    node.father.right = node.right
                    node.father.right_count -= 1
                if node.right:
                    node.right.father = node.father
                self.update(node.father, -1)
                return
        if not node.right:
            if not node.father:
                self.root = node.left
                if self.root:
                    self.root.father = None
                return
            else:
                if node.father.val > node.val:
                    node.father.left = node.left
                    node.father.left_count -= 1
                else:
                    node.father.right = node.left
                    node.father.right_count -= 1
                if node.left:
                    node.left.father = node.father
                self.update(node.father, -1)
                return
        successor = self.successor(node)
        node.val = successor.val
        node.counts = successor.counts
        if successor.father is node:
            successor.father.right = successor.right
            successor.father.right_count -= successor.counts
        else:
            successor.father.left = successor.right
            successor.father.left_count -= successor.counts
        if successor.right:
            successor.right.father = successor.father
        self.update(successor.father, -successor.counts)
    def search_index(self, k):
        node = self.root
        while True:
            if node.left_count + 1 <= k <= node.left_count + node.counts:
                return node.val
            if k > node.left_count + node.counts:
                k = k - node.left_count - node.counts
                node = node.right
            else:
                node = node.left
if __name__ == '__main__':
    bst = BST()
    a = [random.randrange(1, 100) for _ in range(200)]
    differ = len(a) - len(set(a))
    c1 = 0
    c2 = 0
    for n in a:
        e = bst.insert(n)
    for n in a:
        r = bst.remove(n)
        if r == 'no':
            c2 += 1
    print(differ)
    print(c2)