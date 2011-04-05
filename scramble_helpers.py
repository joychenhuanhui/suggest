import itertools, collections, error_model_helpers

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
	print "similarity_model built"
	return model

def char_model(filename):
	f=open(filename)
	model=collections.defaultdict(lambda:1)
	count=0
	for word in f:
		word = word.strip()
		for letter in word:
			model[letter]+=1
			count+=1
	for letter in model.keys():
		model[letter]=float(model[letter])/count
	print "char_model built"
	return model

def probability_index(misspell,correction,char_model):
	miss_letters = collections.defaultdict(lambda:0)
	overlap = collections.defaultdict(lambda:0)
	for letter in misspell:
		miss_letters[letter]+=1
	for letter in correction:
		if miss_letters[letter]>=1:
			overlap[letter]+=1
			miss_letters[letter]-=1
	probability=1
	for letter in overlap.keys():
		probability*=char_model[letter]**overlap[letter]
	return probability

def suggest(word,char_model,similarity_model, error_model):
	word = word.lower()
	similar_words=closest_words(word,similarity_model)
	current_best=("",1)
	for correction in similar_words:
		probability=probability_index(word,correction,char_model)
		if current_best[1] > probability:
			current_best = (correction,probability)
	return (current_best[0], word, current_best[1])

def closest_words(word,model):
	similar_words = set()
	if word >= 6:
		for pre in bigrams(word[:3]):
			for suf in bigrams(word[len(word)-3:]):
				similar_words = similar_words.union(model[pre+suf])
	return similar_words

#similarity_model = similarity_model("corpus")
#char_model = char_model("corpus")
#error_model = error_model_helpers.error_model()
#print suggest("WONDRFUL", char_model, similarity_model, error_model)