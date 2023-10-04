for test in range(int(input())):
    n = int(input())

    if n <= 30:
        print('NO')
    elif (n > 30) and (n - 30 != 6) and (n - 30 != 10) and (n - 30 != 14):
        print('YES')
        print(6, 10, 14, (n-30))
    else:
        print('YES')
        print(6, 10, 15, (n-31))