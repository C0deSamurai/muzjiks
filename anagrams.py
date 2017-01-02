"""This file allows you to find anagrams of tile sets, even with blanks. To avoid an O(n!) running
time complexity, a nonobvious algorithm is used. An anagram dictionary is created that assigns each
letter to a prime number and for every word multiplies together the various prime values of each
letter. In this way, if two words share a prime product they are anagrams, and vice versa.

You can access the dictionary simply by using anagram_dict, or the anagram() function."""


from itertools import combinations_with_replacement

from wordlist_reader import wordlist


primes = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83,
          89, 97, 101)
letters = "ETAOINSHRDLUCMFWYPVBGKJQXZ"
PRIME_VALUES = {letter: prime for letter, prime in zip(letters, primes)}
ANAG_DICT_FILENAME = "anagram_dictionary.dat"


def get_prime_product(letters):
    """Multiplies the prime associated with every letter together and returns the number."""
    val = 1
    for letter in letters:
        val *= PRIME_VALUES[letter.upper()]
    return val


def gen_anagram_dictionary(words):
    """Given a wordlist, generates an anagram dictionary as described earlier. It maps unique
    identifiers to """
    anagram_dict = {}
    for word in words:
        val = get_prime_product(word)
        if val in anagram_dict:
            anagram_dict[val].append(word)
        else:
            anagram_dict[val] = [word]
    return anagram_dict


def write_anagram_dict_to_file(filename, words):
    """Writes a text file with the anagram dictionary to a file for further use."""
    anag_dict = gen_anagram_dictionary(words)
    with open(filename, 'w') as outfile:
        for prod in anag_dict:
            outfile.write("{}: {}\n".format(prod, ' '.join(anag_dict[prod])))
    return None


def read_anagram_dict_from_file(filename):
    """Given a generated anagram dictionary file, reads it in as a dictionary."""
    anag_dict = {}
    with open(filename, 'r') as infile:
        for line in infile:
            prod, anagrams = line[:-1].split(': ')
            prod = int(prod)
            anagrams = anagrams.split(' ')
            anag_dict[prod] = sorted(anagrams)
    return anag_dict


def gen_blanks(num_blanks):
    """Generates every possible blank combination with the given number as an iterable of tuples."""
    return combinations_with_replacement(letters, num_blanks)


def anagram(word):
    """Anagrams the given set of letters. ? stands for a blank: it can be anything. Returns a list
    of anagrams."""
    if '?' in word:
        word_sans_blanks = word.replace('?', '')
        all_anagrams = []
        for letter_combo in gen_blanks(word.count('?')):
            all_anagrams += anagram(word_sans_blanks + ''.join(letter_combo))
        return all_anagrams
    else:
        val = get_prime_product(word)
        return anagram_dict.get(val, [])


# I was going to read this in from a file on startup, but performance testing showed it was just as
# fast to generate it on the spot
anagram_dict = gen_anagram_dictionary(wordlist)
