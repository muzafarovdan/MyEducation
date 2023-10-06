import sys
number = int(sys.stdin.readline())
stack =[]
del_stack = []
for i in range(number):
    a = list(map(int, sys.stdin.readline().split()))
    if a[0] == 1:
        stack.append(a[1])
    else:
        result = stack[-1]
        stack.pop()
        del_stack.append(result)
        
for i in range(len(del_stack)):
    print(str(del_stack[i]))