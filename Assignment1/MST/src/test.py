n = 100
i = 1
while i <= n:
	j = 0
	k = i
	while k%3 == 0:
		k = k/3
		j += 1
	print(i,j)
	i += 1