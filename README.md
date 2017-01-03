# MUZJIKS #

## A Scrabble word finding program ##

This program allows users to find words that fit specific criteria:

 * Anagrams: `XZA` anagrams to `ZAX`, `QUI?` anagrams to `QUIT`, `QUAI`, `QUIN`, `QUID`, `QUIP`, and `QUIZ`.
 * Subanagrams: if you allow any amount of letters, you can form the words `ZAX`, `ZA`, and `AX`
   from the base `XZA`.
 * Pattern matching: if you want to see what words end with UY, search for `*UY`. If you want to see
   how many words have a Q as their penultimate letter, search for `*Q?`.
 * Length: further limit your words to those within a certain length range.
 * Letters that *must* be included or a set of letters that exclude every other word: pattern match
   `AC??` but limit the letters to only `CAEIOU` to get all vowel pairs that follow `AC`, or force
   `E` to be included to mandate that every selected word contain an `E` in it.
 

Front hooks and back hooks are automatically added to the front and back of every word, so by
pattern matching for a single word you will see the hooks.

This is the "spirtual successor" of [Zyzzyva](http://zyzzyva.net/), a program developed by Michael
Thelen. MUZJIKS (as of this writing) does not allow you to use the copyrighted OTCWL2016 word list
or the "cleaned" OSPD5 list, but it does provide the earlier OWL2 and OSPD4 lists as well as other
dictionaries of use to people who play word games that aren't Scrabble or who want to play Scrabble
in languages that aren't English.


Major TODOS:
 * Playability and probability functions?
 * Clean changing dictionaries
 * Snazzy UI
 
 
## A Note on Testing ##
There are helpfully-written unit tests for the anagrams and word_functions modules. If anyone wants
to submit changes, make sure those run without error and also reflect any new features.
