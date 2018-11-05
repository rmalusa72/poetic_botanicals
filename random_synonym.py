# random_synonym.py
# returns a random synonym of a word using wordnet 

import nltk
from nltk.corpus import wordnet as wn
from random import choice

def random_synonym(word):
    synsets = wn.synsets(word)
    synonyms = []
    for synset in synsets:
        for lemma in synset.lemmas():
            synonyms.append(lemma.name())

    print(synonyms)
    synonym = word
    while synonym == word:
        synonym = choice(synonyms)
    return synonym