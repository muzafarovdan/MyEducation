class SegmentTree:
    def __init__(self, array):
        self.length = len(array)
        self.tree = [0] * (4 * self.length)
        self.build(array, 1, 0, self.length - 1)

    def build(self, array, v, tl, tr):
        if tl == tr:
            self.tree[v] = array[tl]
        else:
            tm = (tl + tr) // 2
            self.build(array, 2 * v, tl, tm)
            self.build(array, 2 * v + 1, tm + 1, tr)
            self.tree[v] = self.tree[2 * v] + self.tree[2 * v + 1]

    def update(self, v, tl, tr, pos, new_value):
        if tl == tr:
            self.tree[v] = new_value
        else:
            tm = (tl + tr) // 2
            if pos <= tm:
                self.update(2 * v, tl, tm, pos, new_value)
            else:
                self.update(2 * v + 1, tm + 1, tr, pos, new_value)
            self.tree[v] = self.tree[2 * v] + self.tree[2 * v + 1]

    def query(self, v, tl, tr, l, r):
        if l > r:
            return 0
        if l == tl and r == tr:
            return self.tree[v]
        tm = (tl + tr) // 2
        left_sum = self.query(2 * v, tl, tm, l, min(r, tm))
        right_sum = self.query(2 * v + 1, tm + 1, tr, max(l, tm + 1), r)
        return left_sum + right_sum


length, tests = map(int, input().split())
array = [0] * length
segment_tree = SegmentTree(array)

for _ in range(tests):
    letter, one, two = input().split()
    if letter == 'A':
        segment_tree.update(1, 0, length - 1, int(one) - 1, int(two))
    else:
        print(segment_tree.query(1, 0, length - 1, int(one) - 1, int(two) - 1))
