TPATH = "0643/0643/"
TRAIN = ["ABODAT.643", "APPLING1DAT.643"]

# @brief Returns summary of errors for the minimum edit distance of two words
def minimum_edits(s, t):
	m = len(s)+1
	n = len(t)+1
	d = [[-1]*(n) for x in range(0,m)]
	summary = [[[]]*(n) for x in range(0,m)]

	for i in range(0,m):
		d[i][0] = i
		summary[i][0] = ["I"]*i
	for j in range(0,n):
		d[0][j] = j
		summary[0][j] = ["I"]*j

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
	return summary[m-1][n-1]

def train_abodat(path, model):
	f = open(path, "r")
	for line in f:
		if line[0] == "$":
			continue
		for pair in line.strip().rstrip('.\n').split(','):
			if len(pair) == 0:
				continue
			words = pair.split()
			for error in minimum_edits(words[0], words[1]):
				model[error] += 1
	return model

def train_appling1dat(path, model):
	f = open(path, "r")
	for line in f:
		if line[0] == "$":
			continue
		words = line.split()
		for error in minimum_edits(words[0], words[1]):
			model[error] += 1
	return model

def error_model():
	model = {"D":0, "I":0, "R":0}
	train_abodat(TPATH+TRAIN[0], model)
	train_appling1dat(TPATH+TRAIN[1], model)
	return model

print error_model()