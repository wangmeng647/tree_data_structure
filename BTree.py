import math
import random


class BTreeNode:
    def __init__(self, x=None):
        self.key = [x] if x else []
        self.child = [None, None]
        self.father = None
class BTree:
    def __init__(self, order):
        self.root = BTreeNode()
        self.order = order
    def node_search(self, x):
        node = self.root
        _hot = None
        while node:
            _hot = node
            r = self.index_search(x, node)
            if r < len(node.key) and x == node.key[r]:
                return node
            else:
                node = node.child[r]
        return _hot
    def insert(self, x):
        if not self.root.key:
            self.root.key = [x]
            return
        node = self.node_search(x)
        r = self.index_search(x, node)
        if r < len(node.key) and x == node.key[r]:
            return
        node.key.insert(r, x)
        node.child.append(None)
        while len(node.key) > self.order - 1:
            node = self.overflow(node)
    def overflow(self, node):
        r = self.order // 2
        val = node.key[r]
        node, right_node = self.split(node, r)
        if not node.father:
            self.root = BTreeNode(val)
            self.root.child[0], self.root.child[1] = node, right_node
            node.father, right_node.father = self.root, self.root
            return self.root
        else:
            node_father = node.father
            r = self.index_search(val, node_father)
            node_father.key.insert(r, val)
            node_father.child.insert(r + 1, right_node)
            return node_father
    def index_search(self, x, node):
        for i in range(len(node.key)):
            if x <= node.key[i]:
                break
        return i + 1 if x > node.key[i] else i

    def split(self, node, r):
        right_node = BTreeNode()
        right_node.key = node.key[r + 1:]
        right_node.child = node.child[r + 1:]
        for child in right_node.child:
            if child:
                child.father = right_node
        node.key = node.key[:r]
        node.child = node.child[:r + 1]
        right_node.father = node.father
        return node, right_node
    def successor_search(self, r, node):
        _hot = node
        node = node.child[r + 1]
        while node:
            _hot = node
            node = node.child[0]
        return _hot
    def remove(self, x):
        if not self.root.key:
            return
        node = self.node_search(x)
        r = self.index_search(x, node)
        if r == len(node.key) or node.key[r] != x:
            return
        successor = self.successor_search(r, node)
        if node is not successor:
            node.key[r] = successor.key[0]
            target = successor.key.pop(0)
        else:
            target = successor.key.pop(r)
        if successor is self.root and not successor.key:
            return
        successor.child.pop()
        while successor.father and len(successor.key) < math.ceil(self.order / 2) - 1:
            successor, target = self.underflow(successor, target)
        if not successor.key and successor.child[0]:
            self.root = successor.child[0]
            self.root.father = None
    def underflow(self, node, target):
        node_father = node.father
        r = self.index_search(target, node_father)
        if r < len(node_father.key) and node_father.child[r + 1] and len(node_father.child[r + 1].key) > math.ceil(self.order / 2) - 1:
            r_brother = node_father.child[r + 1]
            node.key.append(node_father.key[r])
            node_father.key[r] = r_brother.key[0]
            node.child.append(r_brother.child[0])
            if r_brother.child[0]:
                r_brother.child[0].father = node
            r_brother.child.pop(0)
            r_brother.key.pop(0)
            return node_father, node_father.key[-1]
        if r > 0 and node_father.child[r - 1] and len(node_father.child[r - 1].key) > math.ceil(self.order / 2) - 1:
            l_brother = node_father.child[r - 1]
            node.key.insert(0, node_father.key[r - 1])
            node_father.key[r - 1] = l_brother.key[-1]
            node.child.insert(0, l_brother.child[-1])
            if l_brother.child[-1]:
                l_brother.child[-1].father = node
            l_brother.child.pop()
            l_brother.key.pop()
            return node_father, node_father.key[-1]
        if r > 0:
            l_brother = node_father.child[r - 1]
            l_brother.key.append(node_father.key[r - 1])
            l_brother.key += node.key
            l_brother.child += node.child
            target = node_father.key.pop(r - 1)
            node_father.child.pop(r)
            return node_father, target
        else:
            r_brother = node_father.child[r + 1]
            node.key.append(node_father.key[r])
            node.key += r_brother.key
            node.child += r_brother.child
            target = node_father.key.pop(r)
            node_father.child.pop(r + 1)
            return node_father, target
a = [random.randrange(1, 100) for _ in range(200)]
b = [random.randrange(1, 100) for _ in range(200)]
b_tree = BTree(20)
for n in a:
    b_tree.insert(n)
for n in b:
    b_tree.remove(n)
ans = []
def dfs(node):
    if not node:
        return
    if len(node.key) > 0:
        for i in range(len(node.key)):
            dfs(node.child[i])
            ans.append(node.key[i])
        dfs(node.child[i + 1])
dfs(b_tree.root)
print(ans)
for i in range(len(ans)):
    for j in range(i + 1, len(ans)):
        if ans[i] > ans[j]:
            print(1)
