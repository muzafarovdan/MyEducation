def count_ways_to_reach_end(N, k):
    dp = [0] * (N + 1)
    dp[1] = 1  # Начальное значение: один способ допрыгнуть в первую клетку

    for i in range(2, N + 1):
        for j in range(1, k + 1):
            if i - j >= 1:
                dp[i] += dp[i - j]

    return dp[N]

# Чтение входных данных
N, k = map(int, input().split())

# Вывод результата
print(count_ways_to_reach_end(N, k))
