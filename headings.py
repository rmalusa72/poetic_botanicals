# headings.py 
# Use text from wikipedia to generate title and factual summary for pages in multimarkdown

import pycorpora
import wikipedia

wikipedia.set_rate_limiting(True)
plants = []
for flower in pycorpora.plants.flowers['flowers']:
    plants.append(flower)
for plant in pycorpora.plants.plants['instruments']:
    plants.append(plant["name"])
plants.sort()

print(plants)

for plant in plants:
    print(plant)
    pagename = wikipedia.search(plant)[0]
    print(wikipedia.summary(pagename)) 
    # account for possibility of disambiguation page
