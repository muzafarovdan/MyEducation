import math
souga = input()
n = len(souga)
dp = []
posougaition = []
for i in range(n):
    dp.append([0] * n)
    posougaition.append([0] * n)
for i in range(n):
    for j in range(n):
        if i == j:
            dp[i][j] = 1
for right in range(n):
    for left in range(right, -1, -1):
        if left == right:
            dp[left][right] = 1
        else:
            minimum = math.inf
            minimumk = -1
            binary1 = souga[left] == '(' and souga[right] == ')'
            binary2 = souga[left] == '[' and souga[right] == ']'
            binary3 = souga[left] == '{' and souga[right] == '}'
            if binary1 or binary2 or binary3:
                minimum = dp[left + 1][right - 1]
            for k in range(left, right):
                if minimum > dp[left][k] + dp[k + 1][right]:
                    minimum = dp[left][k] + dp[k + 1][right]
                    minimumk = k
            dp[left][right] = minimum
            posougaition[left][right] = minimumk
def rec(l, r):
    temp = r - l + 1
    if dp[l][r] == temp:
        return
    if dp[l][r] == 0:
        print(souga[l:r + 1], end="")
        return
    if posougaition[l][r] == -1:
        print(souga[l], end="")
        rec(l + 1, r - 1)
        print(souga[r], end="")
        return
    rec(l, posougaition[l][r])
    rec(posougaition[l][r] + 1, r)
rec(0, n - 1)