# psv.py
# handling phonetic similarity vectors 

import numpy as np
from numpy import dot
from numpy.linalg import norm

# cosine similarity
def cosine(v1, v2):
    if norm(v1) > 0 and norm(v2) > 0:
        return dot(v1, v2) / (norm(v1) * norm(v2))
    else:
        return 0.0

class PSV_Space():

    def __init__(self):
        self.space = dict()
        for line in open("resources/cmudict-0.7b-simvecs", encoding="latin1"):
            line = line.strip()
            word, vec_raw = line.split("  ")
            word = word.lower()
            self.space[word] = np.array([float(x) for x in vec_raw.split()])

    # Return phonetic similarity vector for a word
    def psvector(self, word):
        if word in self.space:
            return self.space[word]
        else:
            return None

    def get_phonetic_similarity(self, word1, word2):
        v1 = self.psvector(word1)
        v2 = self.psvector(word2)
        if isinstance(v1, np.ndarray) and isinstance(v2, np.ndarray):
            similarity = cosine(v1, v2)
        else:
            similarity = 0
        return similarity