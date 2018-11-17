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
        try:
            summary = wikipedia.summary(pagename)
        except wikipedia.exceptions.DisambiguationError as e:
            pagename = e.options[0]
            summary = wikipedia.summary(pagename)
        page = wikipedia.page(title=pagename)
        self.bib.write(pagename + "\n")
        return page.content

    def close(self):
        self.bib.close()
