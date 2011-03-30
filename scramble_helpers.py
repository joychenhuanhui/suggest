import itertools, collections
def bigrams (word):
	for prefix in itertools.combinations(word,2):
		yield ''.join(prefix)

def similarity_model(filename):
	f=open(filename)
	model = collections.defaultdict(lambda: set())
	for word in f:
		word = word.strip()
		if len(word) < 6:
			continue
		for pre in bigrams(word[0:3]):
			for suf in bigrams(word[len(word)-3:]):
				model[pre+suf].add(word)
	return model
	
print similarity_model("corpus")
