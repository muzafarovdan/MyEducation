def find_max_gold_weight(S, n, goldweights):
    dp = [[0] * (S + 1) for _ in range(n + 1)]
 
    for i in range(1, n + 1):
        for j in range(1, S + 1):
            if gold_weights[i-1] <= j:
                dp[i][j] = max(gold_weights[i-1] + dp[i-1][j - gold_weights[i-1]], dp[i-1][j])
            else:
                dp[i][j] = dp[i-1][j]
 
    return dp[n][S]
 
S, n = map(int, input().split())
gold_weights = list(map(int, input().split()))
 
max_weight = find_max_gold_weight(S, n, gold_weights)
print(max_weight)