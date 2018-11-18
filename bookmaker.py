# headings.py 
# Use text from wikipedia to generate title and factual summary for pages in multimarkdown

import re
import pycorpora
import scraper
import synsound
import random

def random_poem_parameters():
    phonetic_similarity_weight = random.randint(0,10)
    metric_conformity_weight = 10 - phonetic_similarity_weight
    line_length_syllables = 10
    poem_length = 100
    score_threshold = random.randint(0, 10)
    switch_odds = random.randint(0, 10)
    parameters = (phonetic_similarity_weight, metric_conformity_weight, line_length_syllables, poem_length, score_threshold, switch_odds)
    return parameters

plants = []
for flower in pycorpora.plants.flowers['flowers']:
    plants.append(flower)
for plant in pycorpora.plants.plants['instruments']:
    plants.append(plant["name"])
plants.sort()

filename = "book/output.txt"
f = open(filename, "w")

scr = scraper.Scraper()

print(plants)
print(len(plants))

for plant in plants[0:5]:

    f.write("# " + plant.title() + "\n")
    text = scr.scrape(plant)
    lines = re.split(r"(?<!syn)\.", text, maxsplit=1)
    f.write("## " + lines[0] + ". ##\n")

    if len(lines) > 1:
        source = lines[1]
    else:
        source = lines[0]

    parameters = random_poem_parameters()
    #f.write(str(parameters) + "\n")
    poem = synsound.poetify(source, parameters)

    f.write("```\n")
    f.write(poem)
    f.write("```\n")

    f.write("<!-- \\newpage -->\n")

f.close()
scr.close()

# print(plants)

# for plant in plants:
#     print(plant)
#     pagename = wikipedia.search(plant)[0]
#     print(wikipedia.summary(pagename)) 
#     # account for possibility of disambiguation page
