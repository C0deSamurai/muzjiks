"""This file combines the word_functions functions to create a "master word search" function that
takes in several predicates and intelligently combines them to return a list of all words that match
the input."""

import anagrams
import word_functions
import wordlist_reader

WORD_FUNCS = {"anagrams": anagrams.anagram, "subanagrams": word_functions.subanagrams, "hooks":
              word_functions.hooks, "back-hooks": word_functions.back_hooks, "front-hooks":
              word_functions.front_hooks, "pattern-match": word_functions.pattern_match}

PRED_FUNCS = {"length-in-range": word_functions.length_in_range, "contains-letters":
              word_functions.contains_letters, "only-contains-letters":
              word_functions.only_contains_letters, "does-pattern-match":
              word_functions.does_pattern_match, "does-anagram": word_functions.does_anagram,
              "does-subanagram": word_functions.does_subanagram}

PREDICATES_TO_FUNCTIONS = {"does-anagram": "anagrams", "does-subanagram": "subanagrams",
                           "pattern-match": "does-pattern-match"}

# there isn't any grand reason for this order, but this is what I thought would make a good guess
# this list is about trading execution time for specificity
FUNCTION_HEURISTIC = ["length-in-range", "only-contains-letters", "contains-letters",
                      "does-anagram", "does-pattern-match", "does-subanagram"]


def master_word_search(queries, dictname="OWL2"):
    """Finds all words in the given lexicon that match the queries. Each query is of the form
    (function_name, *params) where function_name is one of the server's defined function names
    (found in server.py's PRED_FUNCS and WORD_FUNCs) and params are whatever that function needs.

    What this function does is isolate the best query to start pruning with via heuristics: certain
    functions are more computationally intensive or less selective than others, so we identify
    functions that are the most likely to provide fast pruning. From there, we simply chain
    predicates together to achieve the final list. If the first query selected for use is anagrams,
    subanagrams, or pattern matching, it will use the non-predicate versions of those functions for
    further computational improvement.

    One caveat here: returns the empty list if queries is empty."""

    # heuristically identify "useful" functions to start with
    if len(queries) == 0:
        return []

    sorted_queries = sorted(queries, key=lambda x: FUNCTION_HEURISTIC.index(x[0]))
    if sorted_queries[0][0] in PREDICATES_TO_FUNCTIONS:  # replace with non-predicate version
        predname, *params = sorted_queries[0]
        curr_words = WORD_FUNCS[PREDICATES_TO_FUNCTIONS[predname]](*params, dictname="OWL2")
    else:
        predname, *params = sorted_queries[0]
        curr_words = [word for word in wordlist_reader.wordlist(dictname)
                      if PRED_FUNCS[predname](*params, word)]

    for query in sorted_queries[1:]:
        predname, *params = query
        curr_words = [word for word in curr_words if PRED_FUNCS[predname](*params, word)]

    return curr_words
