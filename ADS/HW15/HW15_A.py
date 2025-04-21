import math

def prime_factors(n):
    factors = []
    # Проверяем деление на 2
    while n % 2 == 0:
        factors.append(2)
        n = n // 2

    # Проверяем деление на нечетные числа
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        while n % i == 0:
            factors.append(i)
            n = n // i

    # Если остался простой множитель больше 2
    if n > 2:
        factors.append(n)

    return factors

# Пример использования
number = int(input())
result = prime_factors(number)
print(*result)
