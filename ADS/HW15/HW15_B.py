import math

data = list(map(int, input().split()))

gcd = math.gcd(*data)
lcm = math.lcm(*data)

print(gcd, lcm)