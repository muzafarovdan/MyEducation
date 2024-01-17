tests = int(input())

for test in range(tests):
    n = int(input())
    array = list(map(int, input().split()))

    # Находим индексы первой и последней 1
    l = array.index(1)
    r = n - 1 - array[::-1].index(1)

    # Вычисляем количество 0 между первой и последней 1
    result = array[l:r].count(0)
    print(result)
