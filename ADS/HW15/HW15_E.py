def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    else:
        d, x, y = extended_gcd(b, a % b)
        return d, y, x - y * (a // b)

t = int(input())
testcases = [list(map(int, input().split())) for _ in range(t)]

results = []
for i in range(t):
    a, b = testcases[i]
    d, x, y = extended_gcd(a, b)
    results.append((x, y))

for x, y in results:
    print(f"{x} {y}")
