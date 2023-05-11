
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def creat_tree_mid_order(lis):
    if not lis:
        return None
    head = node = TreeNode(lis.pop(0))
    que = []
    que.append(node)
    while lis:
        node = que.pop(0)
        if lis[0] is not None:
            node.left = TreeNode(lis.pop(0))
            que.append(node.left)
        else:
            lis.pop(0)
        if lis:
            if lis[0] is not None:
                node.right = TreeNode(lis.pop(0))
                que.append(node.right)
            else:
                lis.pop(0)
    return head

