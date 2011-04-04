# @brief Returns summary of errors for the minimum edit distance of two words
def minimum_edits(s, t):
	m = len(s)+1
	n = len(t)+1
	d = [[-1]*(n) for x in range(0,m)]
	summary = [[-1]*(n) for x in range(0,m)]
	
	for i in range(0,m):
		d[i][0] = i
		summary = ("ADD")
	for j in range(0,n):
		d[0][j] = j
		summary = ("ADD")

	for j in range(1,n):
		for i in range(1,m):
			if s[i-1] == t[j-1]:
				d[i][j] = d[i-1][j-1]
			else:
				d[i][j] = min(
				d[i-1][j]+1,
				d[i][j-1]+1,
				d[i-1][j-1]+1)
	print summary