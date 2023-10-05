import sys
length = int(sys.stdin.readline())
massiv = list(map(int, sys.stdin.readline().split()))
massiv.sort()

number = int(sys.stdin.readline())
item = []

def find_right(array, r_val):
    l = -1
    r = len(array)

    while abs(r-l) > 1:
        m = (l+r) // 2
        if array[m] > r_val:
            r = m
        else:
            l = m
    return l

def find_left(array, l_val):
    l = -1
    r = len(array)

    while abs(r-l) > 1:
        m = (l+r) // 2
        if array[m] >= l_val:
            r = m
        else:
            l = m
    return r
    
for i in range(number):
    a, b = map(int, sys.stdin.readline().split())
    left = find_right(massiv, b)
    right = find_left(massiv, a)

    item.append(right - left+1)
        
print(" ".join([str(i) for i in item]))