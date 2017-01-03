"""This file exposes the word functions defined in word_functions.py and the anagram function
defined in anagram.py into a web service that takes in a function name and a string and
returns JSON output."""


import wordlist_reader
from total_word_search import PRED_FUNCS, WORD_FUNCS, master_word_search

import flask

app = flask.Flask(__name__)


def make_int_if_int(string):
    """If the string is a valid integer, returns the integral form of it, otherwise returns the
    string."""
    if all([c in "0123456789" for c in string]):
        return int(string)
    else:
        return string


@app.route("/<dictname>/<function>/<query>", methods=["GET"])
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
        args = [make_int_if_int(x) for x in args]
        return flask.jsonify(PRED_FUNCS[function](*args))


@app.route("/<dictname>/search/<queries>")
def execute_master_search(dictname, queries):
    """Takes in a query string (underscores separate arguments, tildes separate different
    predicates, and returns a JSON list of every word that meets the given criteria."""
    query_strings = queries.split('~')
    query_strings = [q.split('_') for q in query_strings]
    query_strings = [[make_int_if_int(x) for x in q] for q in query_strings]

    return flask.jsonify(master_word_search(query_strings, dictname))


@app.route("/list-lexicons", methods=["GET"])
def list_valid_lexicons():
    """Lists all valid dictionary names as a JSON list."""
    return flask.jsonify(list(wordlist_reader.DICTIONARIES))
