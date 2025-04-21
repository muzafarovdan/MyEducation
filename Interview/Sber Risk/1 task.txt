def deepest_level(data):
    if isinstance(data, dict):
        return max([deepest_level(value) for value in data.values()], default=0) + 1
    elif isinstance(data, list):
        return max([deepest_level(item) for item in data], default=0)
    else:
        return 1
    

# Функция при глубине 3
def sum_3(data):
    for key, value in data.items():
        for m in range(len(value)):
            if isinstance(value[m], list):
                value[m] = sum(value[m])
            elif isinstance(value[m], dict):
                value[m] = sum(value[m].values())
    return data

# Функция при глубине 2
def sum_2(data):
    for key, value in data.items():
        if isinstance(value, list):
            data[key] = sum(value)
        elif isinstance(value, dict):
            data[key] = sum(value.values())
    return data

# Функция при глубине 1
def sum_1(data):
    if isinstance(data, dict):
        return sum(data.values())
    else:
        return data

def forward(data):
    deepest_level_res = deepest_level(data)
    if deepest_level_res == 3:
        data = sum_3(data)  
    elif (deepest_level_res == 2) and all(isinstance(value, list) and len(value) != 1 for value in data.values()):
        data = sum_2(data)
    elif deepest_level_res == 2 and all((isinstance(value, list) and len(value) == 1) or isinstance(value, int) for value in data.values()):
        data = sum_1(data)
    elif (deepest_level_res == 1):
        data = sum_1(data)
    return data

data_dict = {'a': [1, [2, 3, 4], [5, 6, 7]], 'b': [{'c':8, 'd':9}, {'e':3, 'f':4}, 8]}

print(forward(forward(forward(data_dict))))
