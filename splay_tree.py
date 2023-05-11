import random


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
        self.father = None
        self.height = 0

class SplayTree:
    def __init__(self, x=None):
        self.root = TreeNode(x) if x else None

    def search_node_only(self, x):
        if not self.root:
            return None
        node = self.root
        while True:
            if node.val == x:
                return node
            elif x < node.val:
                if not node.left:
                    return node
                node = node.left
            else:
                if not node.right:
                    return node
                node = node.right
    def search(self, x):
        node = self.search_node_only(x)
        if node is self.root:
            return
        self.splay(node)
    def splay(self, node):
        while node.father and node.father.father:
            q = g = node.father.father
            p = node.father
            v = node
            g_father = g.father
            if self.is_l_child(v):
                if self.is_l_child(p):
                    node = self.zig(self.zig(g))
                else:
                    p = self.zig(p)
                    g.right, p.father = p, g
                    node = self.zag(g)
            else:
                if self.is_r_child(p):
                    node = self.zag(self.zag(g))
                else:
                    p = self.zag(p)
                    g.left, p.father = p, g
                    node = self.zig(g)
            node.father = g_father
            if g_father:
                if g_father.left is q:
                    g_father.left = node
                else:
                    g_father.right = node
        if node.father:
            if self.is_l_child(node):
                node = self.zig(node.father)
            else:
                node = self.zag(node.father)
        self.root = node
        self.root.father = None

    def insert(self, x):
        if not self.root:
            self.root = TreeNode(x)
        else:
            self.search(x)
            if self.root.val == x:
                return
            elif self.root.val > x:
                node = TreeNode(x)
                node.left = self.root.left
                if self.root.left:   # left right is None
                    self.root.left.father = node
                node.father = self.root
                self.root.left = node
            else:
                node = TreeNode(x)
                node.right = self.root.right
                if self.root.right:  # left right is None
                    self.root.right.father = node
                node.father = self.root
                self.root.right = node


    # if node is root, update father to be None
    def zig(self, node):
        if not node.left:
            return
        else:
            p = node.left
            node.left = p.right
            node.father = p
            p.right = node
            if node.left:
                node.left.father = node
            return p
    def zag(self, node):
        if not node.right:
            return
        else:
            p = node.right
            node.right = p.left
            node.father = p
            p.left = node
            if node.right:
                node.right.father = node
            return p

    def is_l_child(self, node):
        if not node.father or node.father.right is node:
            return False
        return True
    def is_r_child(self, node):
        if not node.father or node.father.left is node:
            return False
        return True
    def has_r_child(self, node):
        return True if node.right else False
    def has_l_child(self, node):
        return True if node.left else False
    def remove(self, x):
        self.search(x)
        if not self.root or self.root.val != x:
            print('no value found')
        else:
            left = self.root.left
            right = self.root.right
            if right:
                right.father = None
                self.root = right
                self.search(x)
                self.root.left = left
                if left:
                    left.father = self.root
            else:
                self.root = left
                if self.root:
                    self.root.father = None
    def update_height(self, node):
        pre = node.height
        height_l = -1 if not node.left else node.left.height
        height_r = -1 if not node.right else node.right.height
        node.height = max(height_l, height_r) + 1
        return True if pre != node.height else False


s = SplayTree()
a = [random.randrange(1, 100) for _ in range(500)]
differ = len(a) - len(set(a))
c = 0
for n in a:
    s.insert(n)
for n in a:
    r = s.remove(n)
    if r == 'no':
        c += 1
print(c)
print(differ)

