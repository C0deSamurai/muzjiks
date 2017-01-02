"""This file just provides a mechanism for parsing the definitions and syntax of the OWL2 word list
and any others that may be collected. The goal is to simply type "from wordlist_reader import
wordlist" and instantly gain access to a raw sorted list (alphabetical order) that contains every
word in the OWL2. There are other functions for getting definitions and word forms.

"""

import re


def import_text_file(filename):
    """Given a text file, strips the whitespace and splits into lines, returning a list in the
    original order."""
    with open(filename, 'r') as infile:
        return [line.strip() for line in infile]

wordlist = import_text_file("OWL2.txt")


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
            for match in re.finditer(r"-([A-Z]+)",defs):
                words.append(word + match.group(1))

            for entry in words:
                definitions[entry] = defs

    return definitions

# word_definitions = gen_definitions("OWL2_with_info.txt")
# does not work right now lol


def check(word):
    """Case-insensitively checks a word. Returns True if it is valid, and False otherwise."""
    return word.upper() in wordlist
