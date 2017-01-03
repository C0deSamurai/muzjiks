import anagrams
import unittest


class TestAnagrams(unittest.TestCase):

    def test_empty_string(self):
        self.assertEqual(anagrams.anagram(""), [])

    def test_basic_words(self):
        self.assertSetEqual(set(anagrams.anagram("EAT")), {"EAT", "ETA", "ATE", "TEA", "TAE",
                                                           "ETA"})

    def test_blank(self):
        self.assertSetEqual(set(anagrams.anagram("ZED?")), {"ADZE", "DAZE", "DOZE", "ZEDS"})

    def test_lowercase_basic_word(self):
        for string in ("ETA", "eta", "AtE", "Tea"):
            self.assertListEqual(anagrams.anagram(string), anagrams.anagram("TEA"))

    def test_dictionary_choice(self):
        # POBOY is in OWL2 but not OWL1
        self.assertNotEqual(anagrams.anagram("POOBY", "OWL2"), anagrams.anagram("POOBY", "OWL"))


if __name__ == "__main__":
    unittest.main()
