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
        for line in open("cmudict-0.7b-simvecs", encoding="latin1"):
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