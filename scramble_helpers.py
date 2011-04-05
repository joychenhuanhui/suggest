import itertools, collections, error_model_helpers

# @brief Combinatorially generate all bigrams for string, return with yield
# Combinatorially generates all possible bigrams for some word. So in the case
# of the string "xyz", we would generate ["xy", "xz", "yz"]. Note that the
# order of these letters is preserved in these bigrams (i.e., "xy" is
# generated, but "yx" never is).
#
# @param word The word to combinatorially generate bigrams for
#
# @return Yield each particular bigram as it is generated
def combinatorial_bigrams (word):
	for prefix in itertools.combinations(word,2):
		yield ''.join(prefix)

# @brief Build our similarity model
# Build the similarity model. The similarity model is used to find words that
# are "similar" to some word. The real trick is defining what similarity is.
#
# Our current implementation finds word that begin and end in roughly the same
# way. In the case of the malformed word "rcaeacr", we can see that the words
# "research" and "racecar" both begin and end sort of the same. This is the
# noisy approximation that our method tries to accomplish.
#
# Given some particular word, the specific way this method does this is to
# combinatorially generate bigrams out of the beginning and ending trigrams
# of that word. So in the case of "racecar", we take "rac" (the beginning
# trigram) and "car" (the ending trigram) and use combinatorial_bigrams() to
# generate the bigrams for each. This should give us some collection of
# bigrams like "rc", "ra", and "ac".
#
# After this, we want to create a similarity index that people will actually
# use to find words similar to some other word. We build the similarity index
# by combinatorially combining all possible bigrams generated from the
# beginning trigram with all the possible bigrams generated from the ending
# trigram. So in the above example, this would produce strings like "rccr" and
# "raar"; "ra" and "rc" are bigrams generated from the initial trigram of
# "racecar", while "cr" and "ar" are trigrams generated from the final trigram
# of "racecar". Combining them gives us these arbitrary and seemingly useless
# strings.
#
# To generate the similarity model, we just perform this operation on each
# word in a file. We then use this similarity index as a key in a hash table.
# So {"raar":["racecar"]}, although the list at "raar" would contain any and
# all words that have "ra" as a possible initial bigram and "ar" as a possible
# final bigram.
#
# @param filename The filename to build similarity index from; MUST CONTAIN
# ONE WORD PER LINE.
#
# @return A defaultdict object representing the similarity model
def similarity_model(filename):
	f=open(filename)
	model = collections.defaultdict(lambda: set())
	for word in f:
		word = word.strip()
		# OUR EXPERIMENTS DEAL ONLY WITH WORDS GREATER IN LENGTH THAN 6
		if len(word) < 6:
			continue
		# Generating the similarity index described above
		for pre in combinatorial_bigrams(word[0:3]):
			for suf in combinatorial_bigrams(word[len(word)-3:]):
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
		if current_best[1] == probability:
			curr_ed = error_model_helpers.minimum_edits(current_best[0], word)
			new_ed = error_model_helpers.minimum_edits(correction, word)
			if len(new_ed) < len(curr_ed):
				current_best = (correction, probability)
	return (current_best[0], word, current_best[1])

def closest_words(word,model):
	similar_words = set()
	if word >= 6:
		for pre in combinatorial_bigrams(word[:3]):
			for suf in combinatorial_bigrams(word[len(word)-3:]):
				similar_words = similar_words.union(model[pre+suf])
	return similar_words

#similarity_model = similarity_model("corpus")
#char_model = char_model("corpus")
#error_model = error_model_helpers.error_model()
#print suggest("wether", char_model, similarity_model, error_model)