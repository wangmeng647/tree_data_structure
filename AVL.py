import collections
import random


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
        self.father = None
        self.height = 0

class AVL:
    def __init__(self, x=None):
        self.root = TreeNode(x) if x else None

    def search(self, x):
        if not self.root:
            return self.root
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

    def insert(self, x):
        if not self.root:
            self.root = TreeNode(x)
        else:
            node = self.search(x)
            if node.val == x:
                return 'a'
            if node.val < x:
                node.right = TreeNode(x)
                node.right.father = node
            if x < node.val:
                node.left = TreeNode(x)
                node.left.father = node
            while node:
                if self.balance_check(node):
                    if not self.update_height(node):
                        return
                    node = node.father
                else:
                    node_father = node.father
                    is_l = self.is_l_child(node)
                    new_node = self.rebuild(node)
                    if node_father:
                        if is_l:
                            node_father.left = new_node
                        else:
                            node_father.right = new_node
                        new_node.father = node_father
                    else:
                        self.root = new_node
                        self.root.father = None
                    return

    def rebuild(self, node):
        g = node
        if not g.left or (g.right and g.right.height > g.left.height):
            p = g.right
            if not p.left or (p.right and p.right.height >= p.left.height):
                v = p.right
                return self.connect34(g, p, v, g.left, p.left, v.left, v.right)
            else:
                v = p.left
                return self.connect34(g, v, p, g.left, v.left, v.right, p.right)
        else:
            p = g.left
            if not p.right or (p.left and p.left.height >= p.right.height):
                v = p.left
                return self.connect34(v, p, g, v.left, v.right, p.right, g.right)
            else:
                v = p.right
                return self.connect34(p, v, g, p.left, v.left, v.right, g.right)

    def connect34(self, a, b, c, node1, node2, node3, node4):
        a.left, a.right = node1, node2
        if node1:
            node1.father = a
        if node2:
            node2.father = a
        self.update_height(a)
        c.left, c.right = node3, node4
        if node3:
            node3.father = c
        if node4:
            node4.father = c
        self.update_height(c)
        b.left, a.father = a, b
        b.right, c.father = c, b
        self.update_height(b)
        return b
    def update_height(self, node):
        pre = node.height
        height_l = -1 if not node.left else node.left.height
        height_r = -1 if not node.right else node.right.height
        node.height = max(height_l, height_r) + 1
        return True if pre != node.height else False
    def is_l_child(self, node):
        if not node.father or node.father.right is node:
            return False
        return True
    def is_r_child(self, node):
        if not node.fater or node.fater.left is node:
            return False
        return True
    def has_r_child(self, node):
        return True if node.right else False
    def has_l_child(self, node):
        return True if node.left else False
    def successor(self, node):
        node = node.right
        while node.left:
            node = node.left
        return node
    def remove(self, x):
        node = self.search(x)
        if not node or node.val != x:
            print('no value found')
            return 'no'
        if not node.left:
            if not node.father:
                self.root = node.right
                if self.root:
                    self.root.father = None
                return
            else:
                if self.is_l_child(node):
                    node.father.left = node.right
                else:
                    node.father.right = node.right
                if node.right:
                    node.right.father = node.father
                update_node = node.father
        elif not node.right:
            if not node.father:
                self.root = node.left
                if self.root:
                    self.root.father = None
                return
            else:
                if self.is_l_child(node):
                    node.father.left = node.left
                else:
                    node.father.right = node.left
                if node.left:
                    node.left.father = node.father
                update_node = node.father
        else:
            successor = self.successor(node)
            node.val = successor.val
            if successor.father is node:
                node.right = successor.right
            else:
                successor.father.left = successor.right
            if successor.right:
                successor.right.father = successor.father
            update_node = successor.father
        self.del_height_update(update_node)

    def balance_check(self, node):
        height_l = -1 if not node.left else node.left.height
        height_r = -1 if not node.right else node.right.height
        return True if abs(height_l - height_r) <= 1 else False
    def del_height_update(self, node):
        while node:
            if self.balance_check(node):
                if not self.update_height(node):
                    return
                node = node.father
            else:
                node_father = node.father
                is_l = self.is_l_child(node)
                new_node = self.rebuild(node)
                if node_father:
                    if is_l:
                        node_father.left = new_node
                    else:
                        node_father.right = new_node
                    new_node.father = node_father
                    node = node_father
                else:
                    self.root = new_node
                    self.root.father = None
                    return
avl = AVL()
counts = collections.defaultdict(int)
def check():
    a = [random.randrange(1, 500) for _ in range(1000)]
    differ = len(a) - len(set(a))
    c = 0
    for n in a:
        avl.insert(n)
    for n in a:
        r = avl.remove(n)
        if r == 'no':
            c += 1
    ans = []
    for k, v in counts.items():
        if v > 1:
            ans.append([k, v])
    return [differ, c, ans, a]
'''for _ in range(50):
    res = check()
    if res[0] != res[1]:
        break
    counts.clear()'''
ans = []
def dfs(node):
    if not node:
        return
    dfs(node.left)
    ans.append(node.val)
    dfs(node.right)
a = [random.randrange(1, 500) for _ in range(100)]
for i in a:
    avl.insert(i)
dfs(avl.root)
print(ans)
for i in range(len(ans)):
    for j in range(i + 1, len(ans)):
        if ans[i] >= ans[j]:
            print(1)