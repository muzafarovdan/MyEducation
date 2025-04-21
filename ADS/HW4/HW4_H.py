class MaxHeap:
    def __init__(self):
        self.heap = []

    def insert(self, x):
        self.heap.append(x)
        self._heapify_up()

    def extract_max(self):
        if len(self.heap) == 0:
            return None
        if len(self.heap) == 1:
            return self.heap.pop()
        
        max_value = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._heapify_down()
        return max_value

    def _heapify_up(self):
        index = len(self.heap) - 1
        while index > 0:
            parent_index = (index - 1) // 2
            if self.heap[index] > self.heap[parent_index]:
                self.heap[index], self.heap[parent_index] = self.heap[parent_index], self.heap[index]
                index = parent_index
            else:
                break

    def _heapify_down(self):
        index = 0
        while True:
            left_child_index = 2 * index + 1
            right_child_index = 2 * index + 2
            largest = index

            if left_child_index < len(self.heap) and self.heap[left_child_index] > self.heap[largest]:
                largest = left_child_index

            if right_child_index < len(self.heap) and self.heap[right_child_index] > self.heap[largest]:
                largest = right_child_index

            if largest != index:
                self.heap[index], self.heap[largest] = self.heap[largest], self.heap[index]
                index = largest
            else:
                break


n = int(input())
commands = [input().split() for _ in range(n)]

heap = MaxHeap()
result = []

for command in commands:
    if command[0] == "0":
        x = int(command[1])
        heap.insert(x)
    elif command[0] == "1":
        max_value = heap.extract_max()
        result.append(max_value)

for max_value in result:
    print(max_value)
