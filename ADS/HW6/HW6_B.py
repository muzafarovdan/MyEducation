for i in range(int(input())):
	n, m = map(int, input().split())
	a = []
	for i in range(n):
		a.append([[int(x) for x in input().split()] for i in range(2)]) # a = [[[1,2],[3,4]],[2,4,1,2]]
	flag = False
	for i in range(n):
		flag |= a[i][0][1] == a[i][1][0]
	flag &= m % 2 == 0
	print("YES" if flag else "NO")