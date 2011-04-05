# suggest #

`suggest` is a (toy) spelling corrector. It is an [official entry](https://sites.google.com/site/chenhuanjoysites) for the 2011 [Google Science Fair](http://www.google.com/events/sciencefair/). This repository contains our core implementation of this spelling corrector; for comparison, we also include [Peter Norvig](http://norvig.com/)'s [implementation](http://norvig.com/spell-correct.html) of an edit distance-based spelling corrector.

### Dependencies ###
1. [Birkbeck Spelling Error Corpus](http://www.ota.ox.ac.uk/headers/0643.xml). Download the corpus at the link (check the section marked "availability"). The end result should be that you have a folder "0643/0643". This needs to go in the ROOT DIRECTORY OF THIS REPOSITORY in order for our program to find it.

### RUNNING EXAMPLE EXPERIMENTS ###

After you've gotten the Birkbeck Misspellings Corpus (see dependencies list), running our provided example experiments is pretty simple. Start by downloading this repository, open the directory and run:

`python main.py`

The output should give you the results of 2 well-marked experiments.