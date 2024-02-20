import math
tests = int(input())

for test in range(tests):
    data = list(map(int, input().split()))
    gcd = math.gcd(*data)
    print(gcd)