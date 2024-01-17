import random

class TreapNode:
    def __init__(self, k, p):
        self.key = k
        self.priority = p
        self.size = 1
        self.left = None
        self.right = None

def size(node):
    return node.size if node else 0

def update_size(node):
    if node:
        node.size = 1 + size(node.left) + size(node.right)

def split(node, key):
    if not node:
        return None, None

    if node.key <= key:
        left, right = split(node.right, key)
        node.right = left
        update_size(node)
        return node, right
    else:
        left, right = split(node.left, key)
        node.left = right
        update_size(node)
        return left, node

def merge(left, right):
    if not left:
        return right
    elif not right:
        return left

    if left.priority > right.priority:
        left.right = merge(left.right, right)
        update_size(left)
        return left
    else:
        right.left = merge(left, right.left)
        update_size(right)
        return right

def insert(root, key):
    if not root:
        return TreapNode(key, random.random())

    left, right = split(root, key - 1)
    new_node = TreapNode(key, random.random())
    return merge(merge(left, new_node), right)

def erase(root, key):
    left, right = split(root, key - 1)
    middle, _ = split(right, key)
    del middle
    return merge(left, _)

def kth_max(root, k):
    if not root or k > root.size:
        return -1

    count_right = root.right.size if root.right else 0

    if count_right == k - 1:
        return root.key
    elif count_right >= k:
        return kth_max(root.right, k)
    else:
        return kth_max(root.left, k - count_right - 1)

def process_commands(commands):
    root = None
    result = []

    for command, k in commands:
        if command == 1:
            root = insert(root, k)
        elif command == 0:
            result.append(kth_max(root, k))
        elif command == -1:
            root = erase(root, k)

    return result

def main():
    n = int(input())
    commands = [tuple(map(int, input().split())) for _ in range(n)]

    result = process_commands(commands)

    for res in result:
        print(res)

if __name__ == "__main__":
    main()
