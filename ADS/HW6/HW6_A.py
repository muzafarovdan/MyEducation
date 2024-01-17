import math

tests = int(input())
for test in range(tests):
    a, b = map(int,input().split())
    if a <= 2:
        print(1)
    else:
        print(math.ceil((a - 2) / b) + 1)