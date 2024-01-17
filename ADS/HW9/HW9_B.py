for test in range(int(input())):
    one = 0
    two = 0
    n, t = map(int, input().split())
    a = list(map(int, input().split()))
    visit = [0]*n
    m = t/2
    v = []
    for i in range(n):
        if a[i]>m:
            v.append(1)
        elif a[i] == m:
            if one > two:
                v.append(1)
                two+=1
            else:
                v.append(0)
                one +=1
        else: 
            v.append(0)

    for i in range(n):
        print(v[i], end = " ")
    print()