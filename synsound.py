# synsound.py
# Test of synonym replacement with meter and sound

import re
import thesaurus
import pronouncing 
import psv

STRESSED = True
UNSTRESSED = False
psvs = psv.PSV_Space()

# Estimate the number of syllables in a word (poorly)
def dirtysyllables(word):
    vowels = "aeiouy"
    invowelblock = False
    syllables = 0
    for letter in word:
        if letter in vowels:
            if not invowelblock:
                invowelblock = True
                syllables = syllables + 1
        else:
            invowelblock = False

    return syllables 

# Use pronouncing to get stresses for a word
# Or return string of as many 3s as there are syllables if word is not in pronouncing dict
def get_stresses(phrase):
    words = phrase.split(" ")
    if len(words) == 1:
        return get_stresses_oneword(phrase)
    else:
        stresses = ""
        for word in words:
            stresses = stresses + get_stresses_oneword(word)
        return stresses

def get_stresses_oneword(word):
    phones_list = pronouncing.phones_for_word(word)
    if len(phones_list) > 0:
        phones = phones_list[0]
        stresses = pronouncing.stresses(phones)
    else:
        num_syllables = dirtysyllables(word)
        stresses = '3' * num_syllables
    return stresses

def poetify(sentence):

    poem = []
    next_syllable = UNSTRESSED

    for word in sentence.split(" "):
        # Potential next words are stored in a dictionary with the format
        # word:(stress pattern, phonetic vector, score)
        potential_words = {word:(get_stresses(word), psvs.psvector(word), 0)}

        # Get word's synonyms to add to potential words
        w = thesaurus.Word(word)
        synonyms = w.synonyms()
        for synonym in synonyms:
            potential_words[synonym] = (get_stresses(synonym), psvs.psvector(synonym), 0)

        # Score potential words
        

        


# Attempt synonym replacement to construct metered (currently iambic) text
def poetify_1(sentence):
    
    poem = []
    next_syllable = UNSTRESSED

    for word in sentence.split(" "):
        print(word)

        stresses = get_stresses(word)
        if len(stresses) == 1:
            stresses = "3" # Ignore the stress of one-syllable words
        print(stresses)

        if next_syllable == STRESSED:
            desired_syl_pattern = r"[123]([03][123])*[03]*"
        else:
            desired_syl_pattern = r"[03]([123][03])*[123]*"
        print(desired_syl_pattern)
        print(re.match(desired_syl_pattern, stresses))

        if re.match(desired_syl_pattern, stresses):
            poem.append(word)
            if len(stresses) % 2 != 0:
                next_syllable = not next_syllable
        else:
            w = thesaurus.Word(word)
            synonyms = w.synonyms()
            if len(synonyms) > 0:
                good_synonyms = []
                for synonym in synonyms:
                    syn_stresses = get_stresses(synonym)
                    if re.match(desired_syl_pattern, syn_stresses):
                        good_synonyms.append(synonym)
                if len(good_synonyms) > 0:
                    poem.append(good_synonyms[0])
                else:
                    poem.append(word)
            else:
                poem.append(word)

    return poem
