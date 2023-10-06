def is_valid_sequence(s):
    stack = []
    mapping = {")": "(", "]": "[", "}": "{"}
    
    for char in s:
        if char in "({[":
            stack.append(char)
        elif char in ")}]":
            if not stack or stack.pop() != mapping[char]:
                return False

    return not stack

input_string = input()
if is_valid_sequence(input_string):
    print("YES")
else:
    print("NO")