"""This file provides Zyzzyva-like functionality for dealing with words: subanagrams, hooks, etc."""


from anagrams import anagram_dict, gen_blanks, get_prime_product, letters
from wordlist_reader import check, wordlist

import re


def subanagrams(word):
    """Returns a list of every word that can be made from any subset of the letters, including ?'s
    for blanks."""
    if '?' in word:  # blanks
        # Generate all possible combinations of blank letters

        # remove blanks and add them back in
        total_subanagrams = []
        word_sans_blanks = word.replace('?', '')
        for letter_combo in gen_blanks(word.count('?')):
            total_subanagrams += subanagrams(word_sans_blanks + ''.join(letter_combo))
        return list(set(total_subanagrams))
    else:
        base_prod = get_prime_product(word.upper())
        total_subanagrams = []
        for prod in anagram_dict:
            if base_prod % prod == 0:  # subanagram
                total_subanagrams += anagram_dict[prod]
        return list(set(total_subanagrams))


def regex_search(pattern):
    """Returns all words that match the regex pattern, case-insensitive."""
    modified_pattern = '^' + pattern + '$'  # only match complete words
    return [word for word in wordlist() if re.match(modified_pattern, word, re.IGNORECASE)]


def pattern_match(query):
    """Simply searches for the pattern in the dictionary and returns a list of matches. ? is a
    blank, and * is any number of letters."""
    if '?' in query:  # recursively substitute
        all_patterns = []
        for letter in letters:
            all_patterns += pattern_match(query.replace('?', letter, 1))
        return all_patterns
    elif '*' in query:
        # regex is slow as molasses but I don't know how to make this better
        return regex_search(query.replace('*', '.*'))
    else:
        if check(query):
            return [query]
        else:
            return []


def front_hooks(word):
    """Given a literal word with just letters, finds all letters that can go in front of the
    word, sorted alphabetically."""
    return sorted([letter for letter in letters if check(letter + word.upper())])


def back_hooks(word):
    """Given a literal word, finds all the letters that can be added to the back, sorted
    alphabetically."""
    return sorted([letter for letter in letters if check(word.upper() + letter)])


def hooks(word):
    """Given a literal word, returns a tuple (front, back) with both the front and back hooks of the
    word."""
    return (front_hooks(word), back_hooks(word))


def length_in_range(word, min_len, max_len):
    """Returns True if the word's length is between min_len and max_len, inclusive."""
    return min_len <= len(word) <= max_len


def only_contains_letters(word, tiles):
    """Returns True if and only if there are no letters in the word outside of the iterable
    letters."""
    return all([c in tiles.upper() for c in word.upper()])


def contains_letters(word, tiles):
    """Returns True if and only if every letter in tiles is in word."""
    return all([letter in word.upper() for letter in tiles.upper()])
