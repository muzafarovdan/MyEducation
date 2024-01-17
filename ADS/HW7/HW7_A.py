tests = int(input())

for test in range(tests):
    n,m = map(int, input().split())
    num = list(map(int, input().split()))
    if sum(num) != m:
        print("NO")
    else:
        print("YES")
