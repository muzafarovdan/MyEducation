def is_heap(arr, n):
    for i in range(1, n + 1):
        if 2 * i <= n and arr[i - 1] > arr[2 * i - 1]:
            return "NO"
        if 2 * i + 1 <= n and arr[i - 1] > arr[2 * i]:
            return "NO"
    return "YES"

# Чтение входных данных
n = int(input())
arr = list(map(int, input().split()))

# Проверка и вывод результата
result = is_heap(arr, n)
print(result)
