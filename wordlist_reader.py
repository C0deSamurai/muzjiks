"""This file just provides a mechanism for parsing the definitions and syntax of the OWL2 word list
and any others that may be collected. The goal is to simply type "from wordlist_reader import
wordlist; words = wordlist()" and instantly gain access to a raw sorted list (alphabetical order)
that contains every word in the OWL2 or any other desired dictionary.. There are other functions for
getting definitions and word forms.

"""

from functools import lru_cache
from pathlib import Path
import re


DICTIONARIES = {}
for dict_file in Path("dictionaries/").glob("*.txt"):
    DICTIONARIES[dict_file.stem] = dict_file


def import_text_file(dictname="OWL2"):
    """Given a lexicon name, strips the whitespace and splits into lines, returning a list in the
    original order."""
    with DICTIONARIES[dictname].open() as infile:
        return [line.strip() for line in infile]


@lru_cache(4)  # important, because wordlists are big so we memoize and save some data
def wordlist(dictname="OWL2"):
    """Returns a list of words that correspond to the given lexicon name."""
    return import_text_file(dictname)


def gen_definitions(filename):
    """Given a text file with words and their definitions and word endings, generates a dictionary
    mapping every valid word to a definition."""
    definitions = {}
    with open(filename) as infile:
        for line in infile:
            words = []
            word, *defs = line.split(' ')
            words.append(word)
            defs = ' '.join(defs)
            
            for match in re.finditer(r"-([A-Z]+)", defs):
                words.append(word + match.group(1))

            for entry in words:
                definitions[entry] = defs

    return definitions

# word_definitions = gen_definitions("OWL2_with_info.txt")
# does not work right now lol


def check(word, dictname="OWL2"):
    """Case-insensitively checks a word. Returns True if it is valid, and False otherwise."""
    return word.upper() in wordlist(dictname)
