"""This file provides Zyzzyva-like functionality for dealing with words: subanagrams, hooks, etc."""


from anagrams import anagram_dict, gen_blanks, get_prime_product, letters
from wordlist_reader import check, wordlist

import re


def does_anagram(query, word):
    """Returns True if and only if query, with optional blanks, can anagram to word."""
    # have to be careful when you're clever: with this nifty modulo hack to avoid having to actually
    # anagram anything, blanks are counted as optional which isn't ideal, so make sure that if the
    # query without blanks is at least a subanagram of the word that by adding blanks you get where
    # you need to be
    no_blanks_prod = get_prime_product(query.replace('?', ''))
    goal_prod = get_prime_product(word)
    # the minimum factor that can separate them is all E's, which means that for every blank you
    # multiply the prime product by 2
    return goal_prod % no_blanks_prod == 0 and goal_prod // no_blanks_prod > (2 * query.count('?'))


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


def does_subanagram(query, word):
    """Returns True if the query, with optional blanks, can match the given word."""
    if '?' in query:
        query_sans_blanks = query.replace('?', '')
        for letter_combo in gen_blanks(query.count('?')):
            if does_subanagram(query_sans_blanks + ''.join(letter_combo), word):
                return True
        return False
    else:
        return get_prime_product(query) % get_prime_product(word) == 0


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


def does_pattern_match(query, word):
    """Returns True if and only if the pattern described by query (with ? and/or *) matches word."""
    if '?' in query:
        for letter in letters:
            if does_pattern_match(query.replace('?', letter, 1), word):
                return True
        return False
    else:
        modified_pattern = '^' + query.replace('*', '.*') + '$'
        return bool(re.match(modified_pattern, word, re.IGNORECASE))


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
