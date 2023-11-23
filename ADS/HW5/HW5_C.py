class Node:
    def __init__(self, data):
        self.data = data
        self.left = self.right = None


class Tree:
    def __init__(self):
        self.root = None

    def __find(self, node, parent, value):
        if node is None:
            return None, parent, False

        if value == node.data:
            return node, parent, True

        if value < node.data:
            if node.left:
                return self.__find(node.left, node, value)

        if value > node.data:
            if node.right:
                return self.__find(node.right, node, value)

    def insert(self, obj):
        if self.root is None:
            self.root = obj
            return obj

        s, p, fl_find = self.__find(self.root, None, obj.data)

        if not fl_find and s:
            if obj.data < s.data:
                s.left = obj
            else:
                s.right = obj

        return obj

    def __del_leaf(self, s, p):
        if p.left == s:
            p.left = None
        elif p.right == s:
            p.right = None

    def __del_one_child(self, s, p):
        if p.left == s:
            if s.left is None:
                p.left = s.right
            elif s.right is None:
                p.left = s.left
        elif p.right == s:
            if s.left is None:
                p.right = s.right
            elif s.right is None:
                p.right = s.left

    def __find_min(self, node, parent):
        if node.left:
            return self.__find_min(node.left, node)

        return node, parent

    def del_node(self, key):
        s, p, fl_find = self.__find(self.root, None, key)

        if not fl_find:
            return None

        if s.left is None and s.right is None:
            self.__del_leaf(s, p)
        elif s.left is None or s.right is None:
            self.__del_one_child(s, p)
        else:
            sr, pr = self.__find_min(s.right, s)
            s.data = sr.data
            self.__del_one_child(sr, pr)

    def delete(self, key):
        s, p, fl_find = self.__find(self.root, None, key)

        if not fl_find:
            return None

        if s.left is None and s.right is None:
            self.__del_leaf(s, p)
        elif s.left is None or s.right is None:
            self.__del_one_child(s, p)
        else:
            sr, pr = self.__find_min(s.right, s)
            s.data = sr.data
            self.__del_one_child(sr, pr)

    def exists(self, key):
        s, p, fl_find = self.__find(self.root, None, key)
        return fl_find

    def next(self, value):
        current = self.root
        successor = None

        while current is not None:
            if value < current.data:
                successor = current
                current = current.left
            elif value > current.data:
                current = current.right
            else:
                # Node with the given value found
                if current.right is not None:
                    # If the node has a right subtree, find the minimum in that subtree
                    successor, _ = self.__find_min(current.right, current)
                break

        if successor is not None:
            return successor.data
        else:
            return "none"

    def prev(self, value):
        current = self.root
        predecessor = None

        while current is not None:
            if value > current.data:
                predecessor = current
                current = current.right
            elif value < current.data:
                current = current.left
            else:
                # Node with the given value found
                if current.left is not None:
                    # If the node has a left subtree, find the maximum in that subtree
                    predecessor, _ = self.__find_max(current.left, current)
                break

        if predecessor is not None:
            return predecessor.data
        else:
            return "none"

    def __find_max(self, node, parent):
        if node.right:
            return self.__find_max(node.right, node)

        return node, parent


t = Tree()

while True:
    line = input().split()
    if not line:
        break
    elif line[0] == 'insert':
        t.insert(Node(int(line[1])))
    elif line[0] == 'delete':
        t.delete(int(line[1]))
    elif line[0] == 'exists':
        print(t.exists(int(line[1])))
    elif line[0] == 'next':
        print(t.next(int(line[1])))
    elif line[0] == 'prev':
        print(t.prev(int(line[1])))
