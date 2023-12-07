tests = int(input())

for test in range(tests):
    n, x = map(int,input().split())
    a = list(map(int,input().split()))
    b = list(map(int,input().split()))
    for i in range(n):
        if a[i]+b[n-1-i] <= x:
            continue
        else:
            print('No')
            break
    print('Yes')