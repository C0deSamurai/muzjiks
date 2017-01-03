import word_functions
import unittest


class TestWordFunctions(unittest.TestCase):

    # examples only work for OWL2
    def setUp(self):
        with open("dictname.txt") as cfgfile:
            self.assertEqual(cfgfile.read()[:-1], "OWL2")

    def test_does_anagram(self):
        self.assertTrue(word_functions.does_anagram("QA???", "SQUaB"))
        self.assertTrue(word_functions.does_anagram("MEDICAL", "DECLAIM"))
        self.assertFalse(word_functions.does_anagram("MEDICAL", "LOLNO"))
        self.assertFalse(word_functions.does_anagram("QA???", "QAT"))

    def test_subanagrams(self):
        # test nothing
        self.assertEqual(word_functions.subanagrams(""), [])

        # test a single word with no subanagrams
        self.assertEqual(word_functions.subanagrams("ZA"), ["ZA"])

        # test case and order
        self.assertListEqual(word_functions.subanagrams("MIXD?"),
                             word_functions.subanagrams("xmd?i"))

        # test a single word with many subanagrams
        self.assertSetEqual(set(word_functions.subanagrams("DAZE")),
                            {"DAZE", "ADZE",
                             "ADZ", "ZED",
                             "AD", "AE", "DE", "ED", "ZA"})

        # test a blank with many subanagrams
        self.assertSetEqual(set(word_functions.subanagrams("CJXZ?")),
                            {"COX", "COZ", "ZAX",
                             "AX", "EX", "JO", "OX", "XI", "XU", "ZA"})

        # test a word with lots of subanagrams, but just check the length
        # used anagrammer.com/scrabble/ to check this list
        self.assertEqual(len(word_functions.subanagrams("SATE??")), 3649)

    def test_regex_search(self):
        # test nothing
        self.assertEqual(word_functions.regex_search(""), [])

        # test for words with AEIOUY in that order
        # well-known trivia! answers below
        self.assertSetEqual(set(word_functions.regex_search(".*A.*E.*I.*O.*U.*Y.*")),
                            {"ABSTEMIOUSLY", "SACRILEGIOUSLY", "FACETIOUSLY",
                             "ADVENTITIOUSLY", "AUTOECIOUSLY", })

    def test_pattern_match(self):
        # test nothing
        self.assertEqual(word_functions.pattern_match(""), [])

        # test a literal word, in the dictionary and not in it
        self.assertEqual(word_functions.pattern_match("PYTHON"), ["PYTHON"])
        self.assertEqual(word_functions.pattern_match("JAVASCRIPT"), [])  # *cough* *cough*

        # test the blank with the well-known KNIGHT SWAM mnemonic: every consonant in KNIGHT SWAM is
        # a front hook for AE and no other letters are
        self.assertSetEqual(set(word_functions.pattern_match("?AE")),
                            {x + "AE" for x in "KNIGHTSWAM" if x not in "AEIOU"})

        # test the asterisk by finding every word with double XX (hint: none!)
        self.assertListEqual(word_functions.pattern_match("*XX*"), [])

        # redo the test above and find all words with AEIOUY in that order as a subsequence
        self.assertSetEqual(set(word_functions.pattern_match("*A*E*I*O*U*Y*")),
                            {"ABSTEMIOUSLY", "SACRILEGIOUSLY", "FACETIOUSLY",
                             "ADVENTITIOUSLY", "AUTOECIOUSLY"})

        # combine ? and * to find all the words that start with Z, any letter, and then X
        self.assertSetEqual(set(word_functions.pattern_match("Z?X*")),
                            {"ZAX", "ZAXES"})

    def test_does_pattern_match(self):
        # mostly superfluous because it's a thin wrapper around regex matching, but good to have
        self.assertTrue(word_functions.does_pattern_match("A?A****A*", "ALACARTE"))
        self.assertTrue(word_functions.does_pattern_match("?ACK?ACK*", "backpacking"))
        self.assertFalse(word_functions.does_pattern_match("*A", "carriage"))
        self.assertFalse(word_functions.does_pattern_match("CORRECT?", "NO"))

    def test_front_hooks(self):
        # simple: this should be equivalent to pattern matching, if it isn't say something
        for query in ("ATE", "AE", "EX", "MO", "NERVATE", "VERT", "VERSION"):
            self.assertListEqual(word_functions.front_hooks(query),
                                 sorted([w[0] for w in word_functions.pattern_match('?' + query)]))

    def test_back_hooks(self):
        # simply the same thing as above: use pattern matching
        for query in ("TANK", "LOVE", "GO", "POLICE", "MA"):
            self.assertListEqual(word_functions.back_hooks(query),
                                 sorted([w[-1] for w in word_functions.pattern_match(query + '?')]))

    def test_hooks(self):
        # this is dumb, I can read Python
        for query in ("I", "CANT", "BELIEVE", "IM", "DOING", "THIS"):
            self.assertTupleEqual(word_functions.hooks(query),
                                  (word_functions.front_hooks(query),
                                   word_functions.back_hooks(query)))

    def test_length_in_range(self):
        # also dumb
        for query in ("COME", "ON", "NOW"):
            self.assertTrue(word_functions.length_in_range(query, 2, 4))

        for query in ("I", "CAN", "DO", "COOLER", "THINGS"):
            self.assertFalse(word_functions.length_in_range(query, 7, 9))

    def test_contains_letters(self):
        self.assertTrue(word_functions.contains_letters("DISTASTEFUL", "TAEDS"))
        self.assertFalse(word_functions.contains_letters("DISTASTEFUL", "FOLD"))
        self.assertTrue(word_functions.contains_letters("TEST", ""))
        self.assertFalse(word_functions.contains_letters("", "TEST"))
        self.assertTrue(word_functions.contains_letters("TEST", "set"))

if __name__ == "__main__":
    unittest.main()
