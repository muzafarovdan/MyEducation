import sys
length = int(sys.stdin.readline())
massiv = list(map(int, sys.stdin.readline().split()))
massiv.sort()

number = int(sys.stdin.readline())
item = []
p = 0
q = len(massiv)-1
for i in range(number):
    l, r = map(int, sys.stdin.readline().split())
    while massiv[p] < l and massiv[q] > r:
        if massiv[p] >= l:
            pass
        else:
            p += 1
        if massiv[q] <= r:
            pass
        else:
            q -= 1
    item.append(q-p+1)
        


print(" ".join([str(i) for i in item]))


