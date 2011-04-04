# @brief Returns summary of errors for the minimum edit distance of two words
def minimum_edits(s, t):
	m = len(s)+1
	n = len(t)+1
	d = [[-1]*(n) for x in range(0,m)]
	summary = [[[]]*(n) for x in range(0,m)]

	for i in range(0,m):
		d[i][0] = i
		summary[i][0] = ["I"]
	for j in range(0,n):
		d[0][j] = j
		summary[0][j] = ["I"]

	for j in range(1,n):
		for i in range(1,m):
			if s[i-1] == t[j-1]:
				d[i][j] = d[i-1][j-1]
				summary[i][j] = summary[i-1][j-1]
			else:
				d[i][j] = min(
				d[i-1][j]+1,
				d[i][j-1]+1,
				d[i-1][j-1]+1)

				if d[i-1][j]+1 <= d[i][j-1]+1 and d[i-1][j]+1 <= d[i-1][j-1]+1:
					summary[i][j] = summary[i-1][j] + ["D"]
				elif d[i][j-1]+1 <= d[i-1][j]+1 and d[i][j-1]+1 <= d[i-1][j-1]+1:
					summary[i][j] = summary[i][j-1] + ["I"]
				elif d[i-1][j-1]+1 <= d[i-1][j]+1 and d[i-1][j-1]+1 <= d[i][j-1]+1:
					summary[i][j] = summary[i-1][j-1] + ["R"]
	print summary
	print summary[m-1][n-1]

minimum_edits("exponential", "polynomial")