def count_facing(heights: list) -> list:
    stack = []
    answ = []
    for height in heights:
        if not stack:
            answ.append(0)
        else:
            answ.append(len(stack))

        while stack and stack[-1] < height:
            stack.pop()

        stack.append(height)

    return answ

def facing_answer(heights: list, facing: str) -> list:
    left = count_facing(heights)
    heights.reverse()
    right = count_facing(heights)
    answ = []
    for index, value in enumerate(facing):
        if value == 'L':
            answ.append(left[index])
        else:
            answ.append(right[len(right) - 1 - index])
    return answ


input()
heights = list(map(int, input().split()))
facing = input()

print(*facing_answer(heights, facing))
