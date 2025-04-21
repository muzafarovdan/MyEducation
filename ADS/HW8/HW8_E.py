import math
s = input()
n = len(s)
dp = []
for i in range(n):
    dp.append([0] * n)
for i in range(n):
    for j in range(n):
        if i == j:
            dp[i][j] = 1
for right in range(n):
    for left in range(right, -1, -1):
        if left == right:
            dp[left][right] = 1
        else:
            min = math.inf
            mink = -1
            b1 = s[left] == '(' and s[right] == ')'
            b2 = s[left] == '[' and s[right] == ']'
            b3 = s[left] == '{' and s[right] == '}'
            if b1 or b2 or b3:
                min = dp[left + 1][right - 1]
            for k in range(left, right):
                if min > dp[left][k] + dp[k + 1][right]:
                    min = dp[left][k] + dp[k + 1][right]
            dp[left][right] = min
print(n - min)