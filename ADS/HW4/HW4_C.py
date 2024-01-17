import sys

def add_element(val):
    list_queue.insert(0,val)
    return list_queue

def remove_element():
    return list_queue.pop()
list_queue = []
for _ in range(int(input())):
    test = sys.stdin.readline().split()
    if test[0] == '+':
       queue = add_element(test[1])
    elif test[0] == '-':
        print(remove_element())

