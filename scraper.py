# scraper.py
# Grabs text from wikipedia

import wikipedia

class Scraper:

    def __init__(self):
        wikipedia.set_rate_limiting(True)
        filename = "book/pages_used.txt"
        self.bib = open(filename, "w")

    def scrape(self, query):
        pagename = wikipedia.search(query)[0]
        
        success = False
        last_pagename = pagename
        index = 0
        while not success:
            try:
                summary = wikipedia.summary(pagename)
                success = True
            except wikipedia.exceptions.DisambiguationError as e:
                print("Excepting DisambiguationError for " + pagename)
                print("options: " + str(e.options))
                last_pagename = pagename
                pagename = e.options[0]
                if pagename == last_pagename:
                    # Stuck in disambiguation loop
                    index = index + 1
                    if len(e.options) > index:
                        pagename = e.options[index]


        # try:
        #     summary = wikipedia.summary(pagename)
        # except wikipedia.exceptions.DisambiguationError as e:
        #     print("Excepting DisambiguationError")
        #     print(e.options)
        #     pagename = e.options[0]
        #     summary = wikipedia.summary(pagename)


        page = wikipedia.page(title=pagename)
        self.bib.write(pagename + "\n")
        return page.content

    def close(self):
        self.bib.close()
