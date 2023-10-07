import math
import sys

def equation(x, C):
    return x**2 + math.sqrt(x) - C

def find_x(C, precision=1e-6):
    left = 0.0
    right = C
    while right - left > precision:
        mid = (left + right) / 2
        if equation(mid, C) < 0:
            left = mid
        else:
            right = mid
    return left

# Вводим значение C
C = float(sys.stdin.readline())
# Находим x с точностью 1e-6 и выводим результат с 6 знаками после точки
result = find_x(C)
print("{:.6f}".format(result))
