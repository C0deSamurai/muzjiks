from total_word_search import master_word_search

import unittest


class TestTotalWordSearch(unittest.TestCase):
    def test_all(self):
        """Can't think of any way to split this up!"""
        query1 = (("does-pattern-match", "ALAB*"), ("length-in-range", 10, 15))

        # a long running time is indicative of a bad heuristic here
        query2 = (("does-subanagram", "TEAS???"), ("length-in-range", 7, 7),
                  ("contains-letters", "DISRATE"), ("does-pattern-match", "A*"))
        query3 = (("does-anagram", "RAPIERS"), ("does-pattern-match", "A*S"))

        self.assertSetEqual(set(master_word_search(query1)), {"ALABASTERS", "ALABASTRINE"})
        self.assertSetEqual(set(master_word_search(query2)), {"ARIDEST", "ASTRIDE"})
        self.assertSetEqual(set(master_word_search(query3)), set())

if __name__ == "__main__":
    unittest.main()
