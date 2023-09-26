for n in range(int(input())):
    er = 0
    dict_lat = {}
    str_lat = ''
    val_str = int(input())
    for i in range(val_str):
        str_lat += input()
    for i in str_lat:
        if i in dict_lat.keys():
            dict_lat[i] += 1
        else:
            dict_lat[i] = 1
    for i in dict_lat.keys():
        if dict_lat.get(i) % val_str != 0:
            er += 1
            print('NO')
            break
    if er == 0:
        print('YES')
        
        
    
      
