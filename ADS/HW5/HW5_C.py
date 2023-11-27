import random
from sys import stdin


class Node:
    def __init__(self, key):
        self.key = key
        self.priority = random.randint(0, 1000)
        self.left = None
        self.right = None


def split(node: Node, x):
    if node is None:
        return None, None
    if node.key < x:
        left, right = split(node.right, x)
        node.right = left
        return node, right
    else:
        left, right = split(node.left, x)
        node.left = right
        return left, node


def merge(Nleft: Node, Nright: Node):
    if Nleft is None:
        return Nright
    if Nright is None:
        return Nleft
    if Nleft.priority > Nright.priority:
        Nleft.right = merge(Nleft.right, Nright)
        return Nleft
    else:
        Nright.left = merge(Nleft, Nright.left)
        return Nright


def insert(node: Node, x):
    left, right = split(node, x)
    a = merge(left, Node(x))
    return merge(a, right)


def delete(node: Node, x):
    left, right = split(node, x)
    T1, T2 = split(right, x + 1)
    return merge(left, T2)


def exists(node: Node, x):
    while node is not None:
        if node.key == x:
            return 'true'
        if node.key < x:
            node = node.right
        else:
            node = node.left
    if node is None:
        return 'false'


def prev(node: Node, x):
    left, right = split(node, x)
    answer = find_max(left)
    merge(left, right)
    return answer


def next(node: Node, x):
    left, right = split(node, x + 1)
    answer = find_min(right)
    merge(left, right)
    return answer


def find_min(node: Node):
    if node is None:
        return 'none'
    while node is not None:
        res = node
        node = node.left
    return res.key


def find_max(node: Node):
    if node is None:
        return 'none'
    while node is not None:
        res = node
        node = node.right
    return res.key


def inorder(root):
    return inorder(root.left) + [root.key] + inorder(root.right) if root else []


tree = None
lines = stdin.readlines()
for i in lines:
    command, num = i.split()
    if command == 'insert':
        tree = insert(tree, int(num))
    elif command == 'exists':
        print(exists(tree, int(num)))
    elif command == 'next':
        print(next(tree, int(num)))
    elif command == 'prev':
        print(prev(tree, int(num)))
    elif command == 'delete':
        tree = delete(tree, int(num))