import scramble_helpers, norvig

def build_tests():
	similarity_model = scramble_helpers.similarity_model("corpus")
	char_model = scramble_helpers.char_model("corpus")
	error_model = scramble_helpers.error_model_helpers.error_model()

	f = open("test_errors", "r")
	our_correct = 0
	norvig_correct = 0
	count = 0
	for line in f:
		pair = line.split()
		if len(pair[0]) < 6 or len(pair[1]) < 6:
			continue
		our_out = scramble_helpers.suggest(pair[1],char_model,similarity_model, error_model)
		norvig_out = norvig.correct(pair[1].lower())
		if our_out[0].lower() == pair[0].lower():
			our_correct += 1
		if norvig_out.lower() == pair[0].lower():
			norvig_correct += 1
		count += 1
		#print (our_out[0], pair[1],  pair[0])
	print count
	print "our correct: " + str(our_correct/float(count))
	print "norvig correct: " + str(norvig_correct/float(count))

build_tests()
