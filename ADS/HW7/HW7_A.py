import itertools

tests = int(input())
n,m = map(int, input().split())

for test in range(tests):
    num = list(map(int, input().split()))
    perm_set = itertools.permutations(num)
    found_value = False
    for num_i in perm_set:
        s = 0
        for i in range(len(num_i)):
            s += sum([num_i[i+j] / (i+j+1) for j in range(len(num_i)-i)])
            if s == m:
                print('YES')
                found_value = True
                break
        if found_value:
            break
   # не проходит
    
