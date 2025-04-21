def knapsack_with_maxvalue(n, m, weights, values):
    dp = [[0 for _ in range(m + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if weights[i - 1] > j:
                dp[i][j] = dp[i - 1][j]
            else:
                dp[i][j] = max(dp[i - 1][j - weights[i - 1]] + values[i - 1], dp[i - 1][j])

    selected_items = []
    j = m
    for i in range(n, 0, -1):
        if dp[i][j] != dp[i - 1][j]:
            selected_items.append(i)
            j -= weights[i - 1]
            if j == 0:
                break

    selected_items.reverse()

    return len(selected_items), selected_items


def main():
    n, m = map(int, input().split())
    weights = list(map(int, input().split()))
    values = list(map(int, input().split()))

    num_selected, selected_items = knapsack_with_maxvalue(n, m, weights, values)

    print(num_selected)
    print(*selected_items)


if __name__ == "__main__":
    main()
