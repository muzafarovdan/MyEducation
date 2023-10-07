import sys
stack = []
min_values = []
tests = int(sys.stdin.readline())

for _ in range(tests):
    a = list(map(int, sys.stdin.readline().split()))
    if a[0] == 1:
        if min_values == []:
            min_values.append(a[1])
            stack.append(a[1])
        else:
            stack.append(a[1])
            if a[1] < min_values[-1]:
                min_values.append(a[1])
            else:
                pass
    elif a[0] == 2:
        if stack[-1] == min_values[-1]:
            min_values.pop()
        stack.pop()
    elif a[0] == 3:
        print(min_values[-1])