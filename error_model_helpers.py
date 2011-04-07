import operator, itertools

TPATH = "0643/0643/"
TRAIN = ["ABODAT.643", "APPLING1DAT.643", "APPLING2DAT.643"]

# @brief Returns summary of errors for the minimum edit distance of two words
# Computes the Levenshtein distance of two words, returning not the count,
# but a list of the errors themselves. So if there is one replacement, one
# insertion, and one deletion, we return ["R", "I", "D"]. Calling len() on
# this list will give us the minimum edit distance.
#
# This method is confusing, but the algorithm is taken almost directly from
# wikipedia, so if you're confused, go there.
#
# @param s First string in comparison
# @param t Second string in comparison
#
# @return The a list summarizing errors between s and t
def minimum_edits(s, t):
	m = len(s)+1  # these two variables are for convenience purposes
	n = len(t)+1
	# Build list to hold the Levenshtein array; we solve the problem of
	# finding minimum edit distance by "flooding" this array.
	d = [[-1]*(n) for x in range(0,m)]
	# holds the summary corresponding to each space in the Levenshtein array;
	# e.g., ["R", "I", "D"] could be at some location in this array
	summary = [[[]]*(n) for x in range(0,m)]

	# Set up the trivially knowable values for both the summary and the
	# Levenshtein array.
	for i in range(1,m):
		d[i][0] = i
		summary[i][0] = summary[i-1][0]+["I"+s[i-1]]
	for j in range(1,n):
		d[0][j] = j
		summary[0][j] = summary[0][j-1]+["I"+t[j-1]]
	# "Flood" the array; the cell at d[m-1][n-1] should at the end be the
	# minimum edit distance. The summary of any cell in d is in the
	# corresponding location in summary, so at the end of this,
	# summary[m-1][n-1] will be returned.
	for j in range(1,n):
		for i in range(1,m):
			# If the letters being compared are the same, edit dist doesn't change
			if s[i-1] == t[j-1]:
				d[i][j] = d[i-1][j-1]
				summary[i][j] = summary[i-1][j-1]
			else:
				# log the actual distance
				d[i][j] = min(
				d[i-1][j]+1,    # deletion
				d[i][j-1]+1,    # insertion
				d[i-1][j-1]+1)  # substitution

				# ... and then generate the summary for that distance
				# deletion
				if d[i-1][j]+1 <= d[i][j-1]+1 and d[i-1][j]+1 <= d[i-1][j-1]+1:
					summary[i][j] = summary[i-1][j] + ["D"+s[i-1]]
				# insertion
				elif d[i][j-1]+1 <= d[i-1][j]+1 and d[i][j-1]+1 <= d[i-1][j-1]+1:
					summary[i][j] = summary[i][j-1] + ["I"+t[j-1]]
				# substitution
				elif d[i-1][j-1]+1 <= d[i-1][j]+1 and d[i-1][j-1]+1 <= d[i][j-1]+1:
					#summary[i][j] = summary[i-1][j-1] + ["R"+s[i-1]+t[j-1]]
					summary[i][j] = summary[i-1][j-1] + ["R"+s[i-1]]
	return summary[m-1][n-1]

# @brief Find misspellings trains the error model on them
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

# @brief Find misspellings trains the error model on them
def train_appling1dat(path, model):
	f = open(path, "r")
	for line in f:
		if line[0] == "$":
			continue
		words = line.split()
		for error in minimum_edits(words[0], words[1]):
			model[error] += 1
	return model

# @brief Find misspellings trains the error model on them
def train_appling2dat(path, model):
	f = open(path, "r")
	for line in f:
		if line[0] == "$":
			continue
		words = line.split()
		if len(words) != 2:
			continue
		for error in minimum_edits(words[0], words[1]):
			model[error] += 1
	return model

# @brief Finds the probability that correction is misspelled as malformed
# Finds the list of minimum edits between malformed and correction, calculates
# the probability that those edits occur, and returns them.
#
# @param malformed The malformed word
# @param correction The possible correction for malformed
# @param error_model The error model holding probability of different errors
#
# @return The total probability of the errors in malformed
def error_probability(malformed, correction, error_model):
	return reduce(operator.mul,
	[error_model[error] for error in minimum_edits(malformed, correction)])
		

# @brief Builds error model
# Builds error model; logs each sort of edit ("D", "I", or "R"), and counts
# their occurrences in some misspellings corpus. Then change those counts into
# probabilities by dividing them by the total misspellings we encountered
#
# @return A dictionary containing the probability distribution of errors in corpus
def error_model():
	poss_edits = "DIR"
	letters = "abcdefghijklmnopqrstuvwxyz"
	model = {}
	for product in itertools.product(poss_edits, letters):
		model[''.join(product)] = 0

	train_abodat(TPATH+TRAIN[0], model)
	train_appling1dat(TPATH+TRAIN[1], model)
	train_appling2dat(TPATH+TRAIN[2], model)

	total = sum(model.values())
	for error in model.keys(): model[error] = model[error]/float(total)

	return model

#print minimum_edits("cow", "cod")
error_model = error_model()
