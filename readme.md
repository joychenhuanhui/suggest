# suggest #

`suggest` is a (toy) spelling corrector. It is an [official entry](https://sites.google.com/site/chenhuanjoysites/home) for the 2011 [Google Science Fair](http://www.google.com/events/sciencefair/). This repository contains our core implementation of this spelling corrector; for comparison, we also include [Peter Norvig](http://norvig.com/)'s [implementation](http://norvig.com/spell-correct.html) of an edit distance-based spelling corrector.

### Dependencies ###
1. [Birkbeck Spelling Error Corpus](http://www.ota.ox.ac.uk/headers/0643.xml). Download the corpus at the link (check the section marked "availability"). The end result should be that you have a folder "0643/0643". This needs to go in the ROOT DIRECTORY OF THIS REPOSITORY in order for our program to find it.
2. [Peter Norvig's Spelling Corrector](http://norvig.com/spell-correct.html) This is included.

### Running example experiments ###
After you've gotten the Birkbeck Misspellings Corpus (see dependencies list), running our provided example experiments is pretty simple. Start by downloading this repository, open the directory and run:

`python main.py`

The output should give you the results of 2 well-marked experiments.

## How it works: ##
Spell-checking is easy. Spelling correction is hard. The most obvious way to implement a spelling corrector is to just look at all the possible corrections around a word. e.g., if I have a malformed word "col", we could just combinatorially generate all possible words that could be corrections for this word. Traditionally we only generate all the possible words that can be obtained by either 1 or 2 edits. This is because most misspellings are within an edit distance of 2 (some literature claims this number is as high as 90%). This is the approach taken by Peter Norvig's spelling corrector. He sums this process up pretty well [here](http://norvig.com/spell-correct.html).

The problem is that there are many words that are outside an edit distance of 2, but which are still recoverable. It does not, for example, take a lot of imagination to figure out what the word "emxalpe" gets corrected to. Our approach is to use a noisy approximation to find words that are "most similar" to a malformed word, and then to find which of those is most similar.

### Finding words "like" our malformed word ###
It would be really easy to just look through every word in a very large corpus and simply just return the one that was "most similar" to our malformed word (we'll detail how to do this in a minute), but that is really inefficient. What we want to do instead is to find a way to noisily approximate which words are "like" our malformed word.

We were inspired by facial recognition in image processing. In short, one way to look for faces is to find the SIFT points in a picture, and then compare them using some clustering heuristic to a set of predefined "Eigenfaces". We began by looking for the invariants inside a malformed word -- the things that are not likely to change between a correction and a misspelling, and which help us humans correct a word when we read it.

Probably the best way to do this is to use some sort of phonetics of phonology. But we don't know how to do that. Instead, we noticed that most misspellings still sort of begin and end with the same letters. For example, consider:

`rcaeacr -> racecar`

What we need is a noise-tolerant way to compare the beginnings and endings of a word. What we do is to combinatorially generate all possible pairs of letters from the trigrams at the beginning and end of the word. So for example, in `rcaeacr`, from the trigram at the beginning, the possible bigrams are `rc`, `ra`, and `ca`. Note that we here chose to be sensitive to order.

By combining each of these bigrams with each possible bigram from the ending trigram of the word, we can find a set of words that both begin and end similarly to our malformed word. So in this case, `rcaeacr -> "racecar", "research", ...` and so on. We can see that both racecar and research have similar beginnings and endings to the malformed word. This set of similar words is only 2 words long; typically the set is about 40.

The key advantage here is that, rather than having to compare a malformed word to every other possible word, we only have to compare it to a few other words.

### Comparing Words ###
Now that we have a list of similar words, the only remaining task is to find the possible correction that is *most similar*.

The way we accomplish this is to look at characters that both words have in common. So in the example above:

	rcaecr    <- malformed word
	racecar   <- possible correction
	racecr    <- characters they share (overlap)

We call this sequence of shared characters "**overlap**". Intuitively, we know that the longer the overlap the less likely it is: for example, "a" is an extremely likely overlap -- lots of words have it. In contrast, "sdlkfjsdjksd" is probably an *extremely unlikely* overlap, because few if any words have it.

We use this intuition to develop the probability of a given overlap as an estimator for the probability of a correction being correct. We begin by building a frequency distribution for all the characters in English: we simply count every character in a large corpus and calculate the percent total make up for each. So for example, x might be 0.005% of the total corpus, and would go down as such.

Using the law of total probability, we can establish the probability of an overlap occurring in the wild. So for example, if the overlap is "xq", we know that the overlap will be relatively unlikely, with a probability of around (0.005)*(0.01). Again, the more unlikely overlap is, the more likely that particular correction is.

There is one important exception here. Sometimes two possible corrections have the same overlap for some malformed word. For example, if the malformed word is `dxrector`, then the corrections `director` and `codirector` will have the same overlap.

Solving this case is simple. If we have a tie probability, we pick the correction that has the smallest Levenshtein distance from the word.

At the end of this we output our suggestion.
