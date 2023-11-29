import random
import sys
 
class Node:
    def __init__(self, value):
        self.value = value
        self.size = 1
        self.y = random.randint(0, 1 << 31)
        self.has_zero = False
        self.reverse = False
        self.right = None
        self.left = None
 
def size(x):
    return x.size if x is not None else 0
 
def update(x):
    if x is None:
        return x
    x.size = size(x.left) + size(x.right) + 1
    x.has_zero = (x.value == 0 or (x.left is not None and x.left.has_zero) or
                   (x.right is not None and x.right.has_zero))
    return x
 
def propagate(v):
    if v is not None and v.reverse:
        v.reverse = False
        v.left, v.right = v.right, v.left
        if v.left is not None:
            v.left.reverse = not v.left.reverse
        if v.right is not None:
            v.right.reverse = not v.right.reverse
    return v
 
def merge(a, b):
    if a is None:
        return b
    if b is None:
        return a
    a = propagate(a)
    b = propagate(b)
    if a.y > b.y:
        a.right = merge(a.right, b)
        return update(a)
    else:
        b.left = merge(a, b.left)
        return update(b)
 
def split(v, k):
    if v is None:
        return None, None
    v = propagate(v)
    if size(v.left) >= k:
        tree_left, tree_right = split(v.left, k)
        v.left = tree_right
        return tree_left, update(v)
    else:
        tree_left, tree_right = split(v.right, k - size(v.left) - 1)
        v.right = tree_left
        return update(v), tree_right
 
def get(k, v):
    if v is None:
        return v
    if size(v.left) == k:
        return v
    if size(v.left) > k:
        return get(k, v.left)
    else:
        return get(k - size(v.left) - 1, v.right)
 
def insert(x, v, k):
    p = split(v, k)
    return merge(merge(p[0], x), p[1])
 
def next(v, k):
    if v is None:
        return -1
    if size(v) < k:
        return -1
    t = -1
    if v.left is not None and v.left.has_zero:
        t = next(v.left, k)
    if t != -1:
        return t
    if size(v.left) >= k and v.value == 0:
        return size(v.left)
    if v.right is not None and v.right.has_zero:
        t = next(v.right, k - size(v.left) - 1)
    if t != -1:
        return t + size(v.left) + 1
    return -1
 
def remove_min(v):
    if v.left is None:
        return v.right
    v.left = remove_min(v.left)
    return update(v)
 
def print_tree(v, k, out):
    if v is None:
        return
    v = propagate(v)
    if k <= 0:
        return
    print_tree(v.left, k, out)
    if size(v.left) < k:
        out.write(f"{v.value} ")
    print_tree(v.right, k - size(v.left) - 1, out)
 
def reverse(v, l, r):
    p1 = split(v, r)
    p2 = split(p1[0], l)
    if p2[1] is not None:
        p2[1].reverse = not p2[1].reverse
    return merge(p2[0], merge(p2[1], p1[1]))
 
def main():
    n, m = map(int, input().split())
 
    global root
    root = None
 
    for i in range(n):
        root = insert(Node(i + 1), root, size(root))
 
    for i in range(m):
        l, r = map(int, input().split())
        root = reverse(root, l - 1, r)
 
    print_tree(root, size(root), sys.stdout)
 
if __name__ == "__main__":
    main()