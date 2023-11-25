import sys

class Node:
    def __init__(self, key):
        self.key = key
        self.left = self.right = None


class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, key):
        self.root = self._insert(self.root, key)

    def _insert(self, root, key):
        if not root:
            return Node(key)

        if key < root.key:
            root.left = self._insert(root.left, key)
        elif key > root.key:
            root.right = self._insert(root.right, key)

        return root

    def delete(self, key):
        self.root = self._delete(self.root, key)

    def _delete(self, root, key):
        if not root:
            return root

        if key < root.key:
            root.left = self._delete(root.left, key)
        elif key > root.key:
            root.right = self._delete(root.right, key)
        else:
            if not root.left:
                return root.right
            elif not root.right:
                return root.left

            # Instead of directly updating the key, swap the key with the minimum key in the right subtree
            min_right = self._find_min(root.right)
            root.key = min_right.key
            root.right = self._delete(root.right, min_right.key)

        return root


    def exists(self, key):
        return self._exists(self.root, key)

    def _exists(self, root, key):
        if not root:
            return False
        if key == root.key:
            return True
        elif key < root.key:
            return self._exists(root.left, key)
        else:
            return self._exists(root.right, key)

    def next_element(self, key):
        successor = self._find_next(self.root, key)
        return successor.key if successor else 'none'

    def _find_next(self, root, key):
        successor = None
        while root:
            if key < root.key:
                successor = root
                root = root.left
            elif key > root.key:
                root = root.right
            else:
                if root.right:
                    return self._find_min(root.right)
                break
        return successor

    def prev_element(self, key):
        predecessor = self._find_prev(self.root, key)
        return predecessor.key if predecessor else 'none'

    def _find_prev(self, root, key):
        predecessor = None
        while root:
            if key < root.key:
                root = root.left
            elif key > root.key:
                predecessor = root
                root = root.right
            else:
                if root.left:
                    return self._find_max(root.left)
                break
        return predecessor

    def _find_min(self, root):
        while root.left:
            root = root.left
        return root

    def _find_max(self, root):
        while root.right:
            root = root.right
        return root


def process_operations(operations):
    tree = BinarySearchTree()
    results = []

    for operation in operations:
        try:
            op, *args = operation.split()
            key = int(args[0]) if args else None

            if op == 'insert':
                tree.insert(key)
            elif op == 'delete':
                tree.delete(key)
            elif op == 'exists':
                results.append('true' if tree.exists(key) else 'false')
            elif op == 'next':
                results.append(tree.next_element(key))
            elif op == 'prev':
                results.append(tree.prev_element(key))
        except EOFError:
            break

    return results


if __name__ == "__main__":
    # Read input data until there is no more input
    operations = []
    while True:
        try:
            operation = input()
            if not operation:
                break
            operations.append(operation)
        except EOFError:
            break

    # Process operations
    output = process_operations(operations)

    # Print results
    for result in output:
        print(result)
