stack = []
result = []
number = int(input())
height = list(map(int, input().split()))
look = input()

for i in range(number):
    if look[i] == 'L' and i == 0:
        result.append(0)
    elif look[i] == 'R' and i == number - 1:
        result.append(0)
    elif look[i] == 'L' and i == 1:
        result.append(1)
    elif look[i] == 'L':
        stack.append(height[0])
        for n in range(1,i):
            if height[n] <= min(stack):
                stack.append(height[n])
            else:
                for m in stack:
                    if m <= height[n]:
                        stack.remove(m)
                stack.append(height[n])
        result.append(len(stack))
        stack.clear()
    elif look[i] == 'R' and i == number - 2:
        result.append(1)
    elif look[i] == 'R':         
        stack.append(height[-1])
        for n in range(number-2,i, -1):
            if height[n] <= min(stack):
                stack.append(height[n])
            else:
                for m in stack:
                    if m <= height[n]:
                        stack.remove(m)
                stack.append(height[n])
        result.append(len(stack))
        stack.clear()
print(' '.join([str(i) for i in result]))