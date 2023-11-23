import sys
tests = int(input())
 
for test in range(tests):
    n = int(input())
    if n % 2 == 0:
        print(n // 2)
    else:
        print((n + 1) // 2)