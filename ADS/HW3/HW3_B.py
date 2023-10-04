import sys
for i in range(int(sys.stdin.readline())):
    stack = []
    n = int(sys.stdin.readline())
    list_a = [int(n) for n in sys.stdin.readline().split()]

    for f in list_a:
        if f not in stack:
            stack.append(f)
        if len(stack) >= n:
            break
    
    print(" ".join([str(i) for i in stack]))