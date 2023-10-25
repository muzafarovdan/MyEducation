import sys
def alice(game):
    for i in range(1,len(game)):
        if game[i] != game[i-1]:
            # удаляем оба элемента и передаем ход бобу
        elif len(game) == 0:
            print('DA')
            return game
        elif i == len(game)-1 and game[i] != game[i-1]:
            print('NET') # потому что в таком случае алиса проиграла
            break

def bob(game):
    for i in range(1,len(game)):
        if game[i] != game[i-1]:
            # удаляем оба элемента и передаем ход алисе
        elif len(game) == 0:
            print('NET')
        else:
            return game
        elif i == len(game)-1 and game[i] != game[i-1]:
            print('DA') # потому что в таком случае выигра ла алиса
            break

tests = int(sys.stdin.readline())
for i in range(tests):
    game = [int(n) for n in sys.stdin.readline().split()]
    if len(game) == 2 and game[0] != game[1]:
        print('DA')
    elif len(game) == 2 and game[0] == game[1]:
        print('NET')
    elif len(game) < 2:
        print('NET')
    
    for _ in range(len(game)//2):
        game = alice(game)
        game = bob(game)