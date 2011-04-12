import itertools, collections, error_model_helpers, re

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
	return model

# @brief  Case-sensitive probability distribution for characters in a corpus
# Generates a probability distribution for characters in a corpus. We first
# walk through the entire corpus, counting each character that we find. We
# then approximate the probability that each character occurs by dividing its
# count by the total number of characters in the corpus. So for example, 'x'
# typically is about 0.005%.
#
# We return a hash table of the format {"character": probability}. So in the
# case of "x", we would have something like {"x": 0.005}. NOTE that this
# dictionary is definitely CASE-SENSITIVE by default.
#
# @param filename The corpus to establish the model from; can be any format
#
# @ A defaultdict object; each char is a key and each value is its probability
def char_model(filename):
	f=open(filename)
	model=collections.defaultdict(lambda:1)
	count=0  # total characters we encounter in corpus
	# Count each letter
	for word in f:
		word = word.strip()
		for letter in word:
			model[letter]+=1
			count+=1
	# Turn the counts of letters into a probability
	for letter in model.keys():
		model[letter]=float(model[letter])/count
	return model

# @brief Finds probability that overlap between two words occurs
# Finds the common characters between misspelling and correction and then
# calculates the probability that those common characters occur anywhere
# in the whatever language char_model is built around. Using the law of total
# probability, we know the probability of this sequence is the probability of
# each character multiplied together. This probability is supplied by the
# char_model.
#
# This probability is a good estimator of how likely correction is for
# misspelling: the less likely the overlap is, the less likely it is that
# other words will share that overlap. So a really unique and unlikely overlap
# will indicate that they share a collection of characters that almost no
# other words do. So the smaller the probability we return, the more likely
# this correction is to be a "good" correction.
#
# @brief misspell The misspelled word
# @brief correction The possible correction for misspell
# @brief char_model Probabilistic model of characters; get from char_model()
#
# @return The total probability that the overlap occurs
def probability_index(misspell,correction,char_model):
	# Start by finding the characters that misspell and correction have in
	# common:
	miss_letters = collections.defaultdict(lambda:0)
	overlap = collections.defaultdict(lambda:0)
	for letter in misspell:
		miss_letters[letter]+=1
	for letter in correction:
		if miss_letters[letter]>=1:
			overlap[letter]+=1
			miss_letters[letter]-=1
	# As noted above, we're looking for smallest probability; thus '1' is a
	# safe initial probability
	probability=1
	# Calculate the total probability of the characters both words have in
	# common. Details above.
	for letter in overlap.keys():
		probability*=char_model[letter]**overlap[letter]
	return probability

# @brief Suggests a word for some misspelled word using provided models
# Suggests a possible correction for word based on the provided char_model,
# similarity_model, and error_model. These can all be obtained from their
# respective methods.
#
# @param word The word to correct
# @param char_model Probability distribution for chars in given language
# @param similarity_model Helps us find words that are "like" our misspelling
# @param error_model Probability distribution for spelling errors
#
# @return A tuple of the suggestion, the original word, and the probability
def suggest(word,char_model,similarity_model,word_model_tuple, error_model):
	# Make word lower case and find the possible corrections "like" it.
	word = word.lower()
	similar_words=closest_words(word,similarity_model)
	current_best=("",1)  # Will hold our current-best word and its probability
	                     # in form (word, probability)
	# Cycle through possible corrections and find the "best" correction
	for correction in similar_words:
		correction = correction.lower()
		probability=probability_index(word,correction,char_model)
		"""if correction in word_model_tuple[0]:
			probability *= 1-word_model_tuple[0][correction]/float(word_model_tuple[1])
		else:
			word_model_tuple = (word_model_tuple[0], word_model_tuple[1]+1)
			word_model_tuple[0][correction] = 1
			probability *= 1-word_model_tuple[0][correction]/float(word_model_tuple[1])"""

		edits = error_model_helpers.minimum_edits(correction, word)
		
		total_error_prob = 1
		for edit in edits:
			if re.search("[^a-zA-Z]+", edit) != None or re.search("[^a-zA-Z]+", edit) != None:
				continue
			total_error_prob *= error_model[edit]
		probability -= total_error_prob

		# DEBUGGING
		#print correction, probability

		if current_best[1] > probability:
			current_best = (correction,probability)
		"""
		# TIEBREAKER: lots of words have the same same overlapping characters,
		# e.g., codirector and director for some malformed word "dxrector".
		# All things equal, we want the correction that's closer to the
		# malformed word. So when two corrections have the same overlap, we
		# compute the Levenshtein distance for both and select the word for
		# which this is smaller.
		if current_best[1] == probability:
			curr_ed = error_model_helpers.minimum_edits(current_best[0], word)
			new_ed = error_model_helpers.minimum_edits(correction, word)
			if len(new_ed) < len(curr_ed):
				current_best = (correction, probability)
		"""
	return (current_best[0], word, current_best[1])

# @brief Find words closest to some string; must be longer than 6 chars
# Find words that are most "like" some string; our experiment is only
# concerned with words greater in length than 6 chars, so all words that are
# smalelr are thrown away.
#
# We use a similarity_model (obtained through similarity_model()) to find
# these words that are "like" our string. We do this by generating the
# similarity index for our string (this process is codified in the comment
# for that method) and looking at every word in that similarity space so
# defined.
#
# @param word The word to find closest words of
# @param similarity_model The model we use to find similar words
#
# @return A set() of similar words
def closest_words(word,similarity_model):
	similar_words = set()
	# Our algorithm is only concerned with words longer than 6 chars
	if word >= 6:
		# Find all similar words using the similarity index
		for pre in combinatorial_bigrams(word[:3]):
			for suf in combinatorial_bigrams(word[len(word)-3:]):
				similar_words = similar_words.union(similarity_model[pre+suf])
	return similar_words

"""TESTING STUFF"""
#similarity_model = similarity_model("corpus")
#char_model = char_model("corpus")
#error_model = error_model_helpers.error_model()
#print suggest("wether", char_model, similarity_model, error_model)