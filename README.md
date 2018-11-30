# poetic_botanicals
Generative field guide with poetry for NaNoGenMo 2018

Running bookmaker.py generates a set of poems in book/output.txt, one for each poem in the list of plants scraped from pycorpora, with a list of wikipedia pages referenced in book/pages_used.txt. Right now this output can be formatted by multimarkdown into HTML, but not into functional LaTeX. 

This project uses aparrish's [pronouncingpy](https://github.com/aparrish/pronouncingpy) library and pre-calculated [cmudict phonetic similarity vectors](https://github.com/aparrish/phonetic-similarity-vectors), savoirfairelinux's [num2words](https://github.com/savoirfairelinux/num2words), manwholikespie's [thesaurus](https://github.com/Manwholikespie/thesaurus), and goldsmith's [wikipedia](https://github.com/goldsmith/Wikipedia). 

For the future:
* Scrape illustrations?
* Add text from other sources?
* Build interface to adjust parameters on the fly? 
