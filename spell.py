import collections

ALPH = "abcdefghijklmnopqrstuvxyzABCDEFGHIJKLMNOPQRSTUVXYZ"

def file_to_list(textfile):
	words=[]
	for word in textfile:
		words.append(word.strip())
	return words

def build_counter(words):
	# "counts" the numbers in the file
	dictionary= {}
	for number in words:
		number = number.strip()
		if not number in dictionary:
			dictionary[number]=1
		else:
			dictionary[number]+= 1
	return dictionary

def word_model(words):
	model = build_counter(words)
	return (model, sum(model.values()))

def check_word(word, dictionary):
	# checks if a word is in a previously made dictionary
	return word in dictionary

def check_list(words, dictionary):
	real_words=[]
	for word in words:
		if check_word(word, dictionary):
			real_words.append(word)
	return real_words

def check_char_sub(wrongword, dictionary):
	poss_list=[]
	for i in range(0,len(wrongword)):
		s1 = wrongword[0:i]
		s2 = wrongword[ i+1: len(wrongword)]
		for letter in ALPH:
			#print s1 + letter + s2
			if s1 + letter + s2 == "cod":
				print check_word("cod", dictionary)
			if check_word(s1 +letter +s2, dictionary):
				poss_list.append(s1 + letter +s2)
	return poss_list
	
def word_part(word):
	partitions= []
	for i in range(0, len(word)):
		#(below) partitioning word, putting it in array, putting that array
		#in partitions
		#button turns into [ ['b', 'utton'],...]
		partitions.append([word[0:i+1],word[i+1:len(word)]])
	return partitions

#doesn't account for compound words	
def is_two_words(partitions, dictionary):
	for pair in partitions:
		if pair[1] == "": 
			continue
		if pair[0] in dictionary and pair[1] in dictionary:
			return pair[0] + " " + pair[1]
	return ""

def sub_list(partitions):
	corrections= []
	for i in range(0, len(partitions)):
		first_slice=partitions[i][0]
		length= len(first_slice)
		if length < 1:
			continue
		first_slice=first_slice[0:length-1]
		second_slice=partitions[i][1]
		for letter in ALPH:
			corrections.append(first_slice+letter+second_slice)
	return corrections

def del_list(partitions):
	corrections=[]
	for letter in ALPH:
		corrections.append(letter + partitions[0][0] + partitions[0][1])
	for i in range(0, len(partitions)):
		for letter in ALPH:
			corrections.append(partitions[i][0]+letter+partitions[i][1])
	return corrections

def add_list(partitions):
	corrections=[]
	for i in range(0, len(partitions)):
		first_slice=partitions[i][0]
		length = len(first_slice)
		if length < 1:
			continue
		first_slice=first_slice[0:length -1]
		second_slice=partitions[i][1]
		corrections.append(first_slice+second_slice)
	return corrections


def max_c(corrections, histogram):
	ret_val = ""
	if len(corrections) > 0:
		ret_val= corrections[0]
	else:
		return ""

	for word in corrections:
		if histogram[word] < histogram[ret_val]:
			continue
		elif histogram[word] > histogram[ret_val]:
			ret_val=word
		else:
			continue
	return ret_val


def suggest(word):
	f=open("corpus", "r")
	words=file_to_list(f)
	histogram = build_counter(words)
	if check_word(word,histogram):
		return word
	partitions = word_part(word)
	two_words=is_two_words(partitions,histogram)
	if two_words != "":
		return two_words
	corrections = set(add_list(partitions)+del_list(partitions)+ sub_list(partitions))
	corrections = check_list(corrections,histogram)
	return max_c(corrections, histogram)
				

#print check_char_sub("grandsonn", histogram)
#partitions = word_part("button")
#print suggest("rcaeacr")
