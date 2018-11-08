# headings.py 
# Use text from wikipedia to generate title and factual summary for pages in multimarkdown

import re
import pycorpora
import wikipedia

wikipedia.set_rate_limiting(True)
plants = []
for flower in pycorpora.plants.flowers['flowers']:
    plants.append(flower)
for plant in pycorpora.plants.plants['instruments']:
    plants.append(plant["name"])
plants.sort()

filename = "book/output.txt"
f = open(filename, "w")

for plant in plants:
    f.write("# " + plant.title() + "\n")

    pagename = wikipedia.search(plant)[0]
    try:
        summary = wikipedia.summary(pagename)
    except wikipedia.exceptions.DisambiguationError as e:
        summary = wikipedia.summary(e.options[0])
    lines = re.split(r"(?<!syn)\.", summary)
    firstline = lines[0] + "." + "\n"
    f.write(firstline)

    f.write("<div style=\"page-break-after: always;\"></div>\n")

f.close()

# print(plants)

# for plant in plants:
#     print(plant)
#     pagename = wikipedia.search(plant)[0]
#     print(wikipedia.summary(pagename)) 
#     # account for possibility of disambiguation page
