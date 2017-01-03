"""This file exposes the word functions defined in word_functions.py and the anagram function
defined in anagram.py into a web service that takes in a function name and a string and
returns JSON output."""

import anagrams
import word_functions

import flask


# for automatic URL routing, give each function a URL name
WORD_FUNCS = {"anagram": anagrams.anagram, "subanagrams": word_functions.subanagrams, "hooks":
              word_functions.hooks, "back-hooks": word_functions.back_hooks, "front-hooks":
              word_functions.front_hooks, "pattern-match": word_functions.pattern_match}

# for functions that return True or False and have more than 1 parameter
PRED_FUNCS = {"length-in-range": word_functions.length_in_range, "contains-letters":
              word_functions.contains_letters, "only-contains-letters":
              word_functions.only_contains_letters, "does-pattern-match":
              word_functions.does_pattern_match, "does-anagram": word_functions.does_anagram,
              "does_subanagram": word_functions.does_subanagram}

app = flask.Flask(__name__)


@app.route("/<dictname>/<function>/<query>")
def execute_query(dictname, function, query):
    """Executes the given function on the query. Every function returns a JSON list of words unless it
    is a predicate function, which returns True or False and has many argument separated by
    hyphens. Uses the dictionary name given in the URL if it isn't a predicate function.
    """
    if function in WORD_FUNCS:
        return flask.jsonify(WORD_FUNCS[function](query, dictname))
    else:
        # parse string into arguments
        args = query.split('-')
        # parse integers
        args = [int(x) if all([char in "1234567890" for char in x]) else x for x in args]
        return flask.jsonify(PRED_FUNCS[function](*args))
