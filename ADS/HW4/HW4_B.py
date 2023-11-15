import sys
for _ in range(int(input())):
    s = sys.stdin.readline()
    print('DA' if min(s.count('0'), s.count('1')) % 2 == 1 else 'NET')