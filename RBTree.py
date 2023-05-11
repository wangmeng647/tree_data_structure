import math
import random


class RBTreeNode:
    def __init__(self, x=None):
        self.val = x
        self.left = None
        self.right = None
        self.father = None
        self.color = 'red'
        self.height = 0
class RBTree:
    def __init__(self, x=None):
        self.root = RBTreeNode(x) if x else None

    def is_l_child(self, node):
        if node.father.left is node:
            return True
        return False
    def has_r_child(self, node):
        return True if node.right else False
    def has_l_child(self, node):
        return True if node.left else False
    def search(self, x):
        node = self.root
        _hot = node
        while node:
            _hot = node
            if x == node.val:
                break
            elif x < node.val:
                node = node.left
            else:
                node = node.right
        return _hot
    def sibling(self, node):
        if self.is_l_child(node):
            return node.father.right
        else:
            return node.father.left
    def add_x(self, x, node):
        if x < node.val:
            node.left = RBTreeNode(x)
            node.left.father = node
        else:
            node.right = RBTreeNode(x)
            node.right.father = node
    def connect34(self, a, b, c, node1, node2, node3, node4):
        a.left, a.right = node1, node2
        if node1:
            node1.father = a
        if node2:
            node2.father = a
        #self.update_height(a)
        c.left, c.right = node3, node4
        if node3:
            node3.father = c
        if node4:
            node4.father = c
        #self.update_height(c)
        b.left, a.father = a, b
        b.right, c.father = c, b
        #self.update_height(b)
        b.color = 'black'
        a.color = c.color = 'red'
        return b
    def rebuild(self, node):
        g = node
        if g.left and g.left.color == 'red':
            p = g.left
            if p.left and p.left.color == 'red':
                v = p.left
                return self.connect34(v, p, g, v.left, v.right, p.right, g.right)
            else:
                v = p.right
                return self.connect34(p, v, g, p.left, v.left, v.right, g.right)
        else:
            p = g.right
            if p.right and p.right.color == 'red':
                v = p.right
                return self.connect34(g, p, v, g.left, p.left, v.left, v.right)
            else:
                v = p.left
                return self.connect34(g, v, p, g.left, v.left, v.right, p.right)
    def red_solve(self, node):
        if node.color == 'black':
            return
        brother = self.sibling(node)
        if brother and brother.color == 'red':
            node.color = brother.color = 'black'
            if node.father is not self.root:
                node.father.color = 'red'
                self.red_solve(node.father.father)
        else:
            father_node, grandfather = node.father, node.father.father
            new_node = self.rebuild(father_node)
            new_node.father = grandfather
            if not grandfather:
                self.root = new_node
            else:
                if grandfather.left is father_node:
                    grandfather.left = new_node
                else:
                    grandfather.right = new_node
    def insert(self, x):
        node = self.search(x)
        if not node:
            self.root = RBTreeNode(x)
            self.root.color = 'black'
            return
        if node.val == x:
            return
        self.add_x(x, node)
        self.red_solve(node)
    def successor(self, node):
        node = node.right
        while node.left:
            node = node.left
        return node
    def delete_x_node(self, node):
        if not node.left:
            if not node.father:
                self.root = node.right
                if self.root:
                    self.root.father = None
                return node, node.right, False
            else:
                is_l = self.is_l_child(node)
                if is_l:
                    node.father.left = node.right
                else:
                    node.father.right = node.right
                if node.right:
                    node.right.father = node.father
                return node, node.right, is_l
        elif not node.right:
            if not node.father:
                self.root = node.left
                if self.root:
                    self.root.father = None
                return node, node.left, True
            else:
                is_l = self.is_l_child(node)
                if is_l:
                    node.father.left = node.left
                else:
                    node.father.right = node.left
                if node.left:
                    node.left.father = node.father
                return node, node.left, is_l
        else:
            successor = self.successor(node)
            node.val = successor.val
            if successor.father is node:
                node.right = successor.right
                is_l = False
            else:
                successor.father.left = successor.right
                is_l = True
            if successor.right:
                successor.right.father = successor.father
            return successor, successor.right, is_l


    def remove(self, x):
        node = self.search(x)
        if not node or node.val != x:
            return
        del_node, substitute, is_l = self.delete_x_node(node)
        if not self.root:
            return
        if self.root.color == 'red':
            self.root.color = 'black'
            return
        if del_node.color == 'red':
            return
        if del_node.color == 'black' and substitute:
            substitute.color = 'black'
            return
        if is_l:
            del_node.father.left = del_node
        else:
            del_node.father.right = del_node
        self.double_black_solve(del_node)
    def has_red_child(self, node):
        if (node.left and node.left.color == 'red') or (node.right and node.right.color == 'red'):
            return True
        return False
    def has_child(self, node):
        if node.left or node.right:
            return True
        return False
    def sibling_with_red_child_solve(self, node, sibling):
        father = node.father
        grandfather = father.father
        father_color = father.color
        if self.is_l_child(node):
            if not self.has_child(node):
                node = None
            if sibling.left and sibling.left.color == 'red':
                new_node = self.connect34(father, sibling.left, sibling, node, sibling.left.left, sibling.left.right, sibling.right)
            else:
                new_node = self.connect34(father, sibling, sibling.right, node, sibling.left, sibling.right.left, sibling.right.right)
        else:
            if not self.has_child(node):
                node = None
            if sibling.left and sibling.left.color == 'red':
                new_node = self.connect34(sibling.left, sibling, father, sibling.left.left, sibling.left.right, sibling.right, node)
            else:
                new_node = self.connect34(sibling, sibling.right, father, sibling.left, sibling.right.left, sibling.right.right, node)
        new_node.color = father_color
        new_node.left.color = new_node.right.color = 'black'
        if grandfather:
            if grandfather.left is father:
                grandfather.left = new_node
            else:
                grandfather.right = new_node
            new_node.father = grandfather
        else:
            self.root = new_node
            new_node.father = None

    def sibling_no_red_child_solve(self, node, sibling):
        father = node.father
        sibling.color = 'red'
        if not self.has_child(node):
            if self.is_l_child(node):
                node.father.left = None
            else:
                node.father.right = None
        if father.color == 'red':
            father.color = 'black'
        else:
            if father is self.root:
                return
            self.double_black_solve(father)

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
    def red_sibling_solve(self, node):
        father = node.father
        grandfather = father.father
        if self.is_l_child(node):
            new_node = self.zag(father)
            new_node.color = 'black'
            new_node.left.color = 'red'
        else:
            new_node = self.zig(father)
            new_node.color = 'black'
            new_node.right.color = 'red'
        if grandfather:
            if grandfather.left is father:
                grandfather.left = new_node
            else:
                grandfather.right = new_node
            new_node.father = grandfather
        else:
            self.root = new_node
            new_node.father = None

    def double_black_solve(self, node):
        sibling = self.sibling(node)
        if sibling.color == 'black':
            if self.has_red_child(sibling):
                self.sibling_with_red_child_solve(node, sibling)
            else:
                self.sibling_no_red_child_solve(node, sibling)
        else:
            self.red_sibling_solve(node)
            sibling = self.sibling(node)
            if self.has_red_child(sibling):
                self.sibling_with_red_child_solve(node, sibling)
            else:
                self.sibling_no_red_child_solve(node, sibling)

rbt = RBTree()

a = [random.randrange(1, 500) for _ in range(100)]
#a = [46, 16, 35, 40, 17, 13, 41, 31, 21, 22,1,45]
#a = [45, 10, 24, 1, 26,  28, 43, 14, 9]
'''while True:
    a = [random.randrange(1, 500) for _ in range(1000)]
    try:
        for i in a:
            rbt.insert(i)
        for i in a:
            rbt.remove(i)
    except:
        print(a)
        break'''
for i in range(1000):
    rbt.insert(i)
ans = []
depth = [0]
pre = 'black'
def dfs(pre, node):
    if not node:
        return 0
    if pre == node.color == 'red':
        print('false')
    pre = node.color
    d_l = 1 + dfs(pre, node.left)
    ans.append(node.val)
    d_r = 1 + dfs(pre, node.right)
    return max(d_l, d_r)
d = dfs(pre, rbt.root)
print(d)
print(len(ans))
print()
print(math.log(1000))