n, k = map(int, input().split())
ropes = [int(input()) for _ in range(n)]

left, right = 1, max(ropes)

while left <= right:
    mid = (left + right) // 2
    count = sum(rope // mid for rope in ropes)
    if count >= k:
        left = mid + 1
    else:
        right = mid - 1

print(right)  # Выводим максимальную длину веревок

