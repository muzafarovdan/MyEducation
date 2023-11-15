import sys
# Определение класса для узла дека
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

# Определение класса для дека
class Deque:
    def __init__(self):
        self.front = None
        self.rear = None

    def is_empty(self):
        return self.front is None
    
    def add_front(self, data):
        new_node = Node(data)
        
        if self.is_empty():
            self.front = self.rear = new_node
        else:
            new_node.next = self.front
            self.front.prev = new_node
            self.front = new_node
    
    def add_rear(self, data):
        new_node = Node(data)
        
        if self.is_empty():
            self.front = self.rear = new_node
        else:
            new_node.prev = self.rear
            self.rear.next = new_node
            self.rear = new_node
    
    def remove_front(self):
        if self.is_empty():
            return None
        
        if self.front == self.rear:
            temp = self.front
            self.front = self.rear = None
        else:
            temp = self.front
            self.front = self.front.next
            self.front.prev = None
            
        return temp.data
    
    def remove_rear(self):
        if self.is_empty():
            return None
        
        if self.front == self.rear:
            temp = self.rear
            self.front = self.rear = None
        else:
            temp = self.rear
            self.rear = self.rear.prev
            self.rear.next = None
            
        return temp.data

# Создание дека
deque_1 = Deque()
deque_2 = Deque()

for _ in range(int(input())):
    test = sys.stdin.readline().split()
    if test[0] == 'pushfront':
        if test[1] == 1:
            deque_1.add_front(test[2])
        elif test[1] == 2:
            deque_2.add_front(test[2])
    elif test[0] == 'pushback':
        if test[1] == 1:
            deque_1.add_rear(test[2])
        elif test[1] == 2:
            deque_2.add_rear(test[2])
    elif test[0] == 'popfront':
        if test[1] == 1:
            print(deque_1.remove_front())
        if test[1] == 2:
            print(deque_2.remove_front())
    elif test[0] == 'popback':
        if test[1] == 1:
            print(deque_1.remove_rear())
            print('Hello')
        if test[1] == 2:
            print(deque_2.remove_rear())
            

# # Добавление элементов в начало и конец дека
# my_deque.add_front(10)
# my_deque.add_rear(20)

# # Удаление элементов из начала и конца дека
# item1 = my_deque.remove_front()
# item2 = my_deque.remove_rear()

# Вывод дека
# print(my_deque)
