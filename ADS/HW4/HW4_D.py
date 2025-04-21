class Node:
    def __init__(self, value):
        self.value = value
        self.prev = None
        self.next = None

class Deque:
    def __init__(self):
        self.front = None
        self.back = None

    def push_front(self, value):
        new_node = Node(value)
        if not self.front:
            self.front = self.back = new_node
        else:
            new_node.next = self.front
            self.front.prev = new_node
            self.front = new_node

    def push_back(self, value):
        new_node = Node(value)
        if not self.back:
            self.front = self.back = new_node
        else:
            new_node.prev = self.back
            self.back.next = new_node
            self.back = new_node

    def pop_front(self):
        value = self.front.value
        self.front = self.front.next
        if self.front:
            self.front.prev = None
        else:
            self.back = None
        return value

    def pop_back(self):
        value = self.back.value
        self.back = self.back.prev
        if self.back:
            self.back.next = None
        else:
            self.front = None
        return value

# Функция для обработки команд
def process_commands(commands):
    deque_dict = {}
    result = []

    for command in commands:
        cmd_parts = command.split()
        operation = cmd_parts[0]

        if operation.startswith('push'):
            _, deque_id, value = cmd_parts
            value = int(value)
            if deque_id not in deque_dict:
                deque_dict[deque_id] = Deque()
            if operation == 'pushfront':
                deque_dict[deque_id].push_front(value)
            elif operation == 'pushback':
                deque_dict[deque_id].push_back(value)
        elif operation.startswith('pop'):
            _, deque_id = cmd_parts
            if operation == 'popfront':
                result.append(deque_dict[deque_id].pop_front())
            elif operation == 'popback':
                result.append(deque_dict[deque_id].pop_back())

    return result

# Ввод данных
n = int(input())
commands = [input() for _ in range(n)]

# Обработка команд и вывод результата
result = process_commands(commands)
for value in result:
    print(value)
