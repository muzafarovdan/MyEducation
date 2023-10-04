t = int(input())
for i in range(t):
     a =list(map(int, input().split()))
     c = a[0] - a[1]
     if c % 10 == 0:
          print(abs(c) // 10)
     else:
          print((abs(c) // 10)+ 1)
