tests = int(input())

for test in range(tests):
    while True:
        try:
            n, x = map(int, input().split())
            break
        except ValueError:
            pass

    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    for i in range(n):
        if a[i] + b[n - 1 - i] <= x:
            continue
        else:
            print('No')
            break
    else:
        print('Yes')
