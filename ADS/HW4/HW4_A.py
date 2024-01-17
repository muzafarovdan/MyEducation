tests = int(input())
store = []
for i in range(tests):
    length = int(input())
    result = [1 for n in range(length)]
    store.append(result)
for i in range(tests):
    print(*store[i])

# print(*result, end = '')
