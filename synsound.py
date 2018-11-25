# synsound.py
# Test of synonym replacement with meter and sound

import re
import thesaurus
import pronouncing 
import psv
import random
from num2words import num2words

STRESSED = True
UNSTRESSED = False

PHONETIC_SIMILARITY_WEIGHT = 9
METRIC_CONFORMITY_WEIGHT = 1
LINE_LENGTH_SYLLABLES = 10
POEM_LENGTH = 100
SCORE_THRESHOLD = 6
SWITCH_ODDS = 1

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

    if syllables != 0: 
        return syllables
    else:
        return 1

# Get stresses for each word in a phrase and concatenate them
def get_stresses(phrase):
    words = phrase.split(" ")
    if len(words) == 1:
        return get_stresses_oneword(phrase)
    else:
        stresses = ""
        for word in words:
            stresses = stresses + get_stresses_oneword(word)
        return stresses

# Use pronouncing to get stresses for a word
# Or return string of as many 3s as there are syllables if word is not in pronouncing dict
def get_stresses_oneword(word):
    phones_list = pronouncing.phones_for_word(word)
    if len(phones_list) > 0:
        phones = phones_list[0]
        stresses = pronouncing.stresses(phones)
        if len(stresses) == 0 or len(stresses) == 1:
            stresses = "3"
    else:
        num_syllables = dirtysyllables(word)
        stresses = '3' * num_syllables
    return stresses


def score_metric_conformity(meter, word):
    position_in_meter = 0
    stresses = get_stresses(word)

    hits = 0
    misses = 0

    for stress in stresses:

        if meter[position_in_meter] == "0":
            options = "03"
        elif meter[position_in_meter] == "1":
            options = "123"

        if stress in options:
            hits = hits + 1
            position_in_meter = position_in_meter + 1
            if position_in_meter >= len(meter):
                position_in_meter = 0
        else:
            misses = misses + 1

    if (hits + misses) == 0:
        print("problem scoring conformity of " + word)
    return (hits / (hits + misses))

    
# Gets cosine similarity of two vectors and converts to value between 0 and 1
def score_phonetic_similarity(word1, word2):
    return ((psvs.get_phonetic_similarity(word1,word2) + 1 )/ 2)

# todo: change how meter works to go by whether last syllable is stressed or unstressed rather than num syllables?
def poetify(sentence, parameters=(PHONETIC_SIMILARITY_WEIGHT, METRIC_CONFORMITY_WEIGHT, 
    LINE_LENGTH_SYLLABLES, POEM_LENGTH, SCORE_THRESHOLD, SWITCH_ODDS)):

    poem = []
    next_syllable = UNSTRESSED
    pre_words = re.findall(r"([\d]+[,\d]+|\w+\'?\w*)", sentence)
    words = []

    for word in pre_words:

        # Check if each word is a number
        if not re.search(r"\d", word):
            words.append(word)
        else:
            # If word contains digits, split into digit and non-digit pieces
            word = re.sub(",", "", word)
            split_by_numbers = re.split(r"(\d+)", word)
            for piece in split_by_numbers:
                #print(piece)
                # Convert digits to strings and add non-digit strings
                if re.fullmatch(r"\d+", piece):
                    word_version = num2words(int(piece), lang="en")
                    words = words + re.findall(r"\w+", word_version)
                elif piece != "": 
                    words.append(piece)

    #print(words)

    index = 0 
    num_words = len(words)

    for i in range(0, POEM_LENGTH):

        #print(index)
        word = words[index]

        # Potential next words are stored in a dictionary with the format
        # word: score
        potential_words = {word:0}

        # Get word's synonyms to add to potential words
        w = thesaurus.Word(word)
        synonyms = w.synonyms()
        for synonym in synonyms:
            potential_words[synonym] =  0

        # Score potential words
        maxscore = 0
        maxscoreword = word

        for nextword in potential_words.keys():
            if len(poem) > 0: 
                phonetic_similarity = score_phonetic_similarity(poem[-1], nextword)

                if next_syllable == UNSTRESSED: 
                    meter = "01"
                else:
                    meter = "10"
                metric_conformity = score_metric_conformity(meter, nextword)

                score = phonetic_similarity * PHONETIC_SIMILARITY_WEIGHT + metric_conformity * METRIC_CONFORMITY_WEIGHT
                potential_words[nextword] = score

                if score > maxscore:
                    maxscore = score
                    maxscoreword = nextword

        
        if maxscore < SCORE_THRESHOLD:
            dice = random.randint(0,9)
            if dice < SWITCH_ODDS:
                i = i - 1
                index = random.randint(0, num_words-1)
                #print("switching")
                continue

        index = index + 1
        if index >= num_words:
            index = random.randint(0, num_words-1)

        #print(maxscoreword + str(maxscore))
        poem.append(maxscoreword)
        stresses = get_stresses(maxscoreword)
        if len(stresses) % 2 == 1:
            next_syllable = not next_syllable

    return poem_to_string(poem)

def poem_to_string(poem):
    output = ""
    running_syllable_count = 0
    for item in poem:
        words = item.split(" ")
        for word in words:
            stresses = get_stresses(word)
            syllable_count = len(stresses)
            output = output + word + " "
            running_syllable_count += syllable_count
            if running_syllable_count >= LINE_LENGTH_SYLLABLES:
                running_syllable_count = 0
                output = output + "\n"
    output = output + "\n"
    return output

# todo: change how meter works to go by whether last syllable is stressed or unstressed rather than num syllables?
def poetify_old_2(sentence):

    poem = []
    next_syllable = UNSTRESSED
    pre_words = re.findall(r"([\d]+[,\d]+|\w+\'?\w*)", sentence)
    words = []

    print(pre_words)

    for word in pre_words:

        print(word)

        # Check if each word is a number
        if not re.search(r"\d", word):
            words.append(word)
        else:
            # If word contains digits, split into digit and non-digit pieces
            word = re.sub(",", "", word)
            split_by_numbers = re.split(r"(\d+)", word)
            print(str(split_by_numbers))
            for piece in split_by_numbers:
                print(piece)
                # Convert digits to strings and add non-digit strings
                if re.fullmatch(r"\d+", piece):
                    word_version = num2words(int(piece), lang="en")
                    print(word_version)
                    words = words + re.findall(r"\w+", word_version)
                elif piece != "": 
                    words.append(piece)

    print(words)

    for word in words:

        # Potential next words are stored in a dictionary with the format
        # word: score
        potential_words = {word:0}

        # Get word's synonyms to add to potential words
        w = thesaurus.Word(word)
        synonyms = w.synonyms()
        for synonym in synonyms:
            potential_words[synonym] =  0

        # Score potential words
        maxscore = 0
        maxscoreword = word

        for nextword in potential_words.keys():
            if len(poem) > 0: 
                phonetic_similarity = score_phonetic_similarity(poem[-1], nextword)

                if next_syllable == UNSTRESSED: 
                    meter = "01"
                else:
                    meter = "10"
                metric_conformity = score_metric_conformity(meter, nextword)

                score = phonetic_similarity * PHONETIC_SIMILARITY_WEIGHT + metric_conformity * METRIC_CONFORMITY_WEIGHT
                potential_words[nextword] = score

                if score > maxscore:
                    maxscore = score
                    maxscoreword = nextword

        poem.append(maxscoreword)
        stresses = get_stresses(maxscoreword)
        if len(stresses) % 2 == 1:
            next_syllable = not next_syllable

    return poem_to_string(poem)

# Attempt synonym replacement to construct metered (currently iambic) text
def poetify_old(sentence):
    
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
