def longest_increasing_subsequence(n, a):
    dp = [1] * n
    prev = [-1] * n

    for i in range(1, n):
        for j in range(i):
            if a[i] > a[j] and dp[i] < dp[j] + 1:
                dp[i] = dp[j] + 1
                prev[i] = j

    max_index = max(range(n), key=lambda i: dp[i])

    result = []
    while max_index != -1:
        result.append(a[max_index])
        max_index = prev[max_index]

    result.reverse()
    return len(result), result

n = int(input())
a = list(map(int, input().split()))

length, sequence = longest_increasing_subsequence(n, a)

print(length)
print(*sequence)
