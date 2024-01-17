n = int(input())
stairs = list(map(int, input().split()))
stairs_one = [0 for i in range(n)]
stairs_one[0] = stairs[0]

for i in range(1, n):
    if i == 1:
        stairs_one[i] = max(stairs_one[i - 1], 0) + stairs[i]
    else:
        stairs_one[i] = max(stairs_one[i - 1], stairs_one[i - 2]) + stairs[i]
print(stairs_one[-1])
