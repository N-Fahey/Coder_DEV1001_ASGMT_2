import unittest
from include.game import WordGame
from include.settings import FILEPATH_WORDLIST

class TestWordGame(unittest.TestCase):
    def setUp(self):
        #Create a game object to use for testing
        self.game = WordGame()

    def test_get_wordlist(self):
        #Load the games wordlist and test it matches the loaded wordlist of the game object
        with open(FILEPATH_WORDLIST) as f:
            expected_word_list = [line.replace('\n','') for line in f.readlines()]
            self.assertEqual(self.game._wordlist, expected_word_list)
        #Test that wordlist is None when the wordlist path doesn't exist
        self.assertIsNone(self.game._get_wordlist('this/path/doesnt/exist/wordlist.txt'))

    def test_choose_random_word(self):
        #Test that a random word is chosen from the wordlist
        self.game._choose_random_word()
        self.assertIn(self.game._solution, self.game._wordlist)
        #Test that AttributeError is raised if trying to choose random word when wordlist is None
        self.game._wordlist = None
        self.assertRaises(AttributeError, self.game._choose_random_word)

    def test_check_guess(self):
        #Test that a correct guess returns True
        self.game._solution = 'apple'
        result = self.game._check_guess('apple')
        self.assertTrue(result)

        #Test that an incorrect guess returns False
        result = self.game._check_guess('smelt')
        self.assertFalse(result)

        #Test that an incorrect guess is formatted correctly
        self.game._solution = 'pooch'
        self.game._check_guess('proof')
        self.assertEqual(self.game._guesses[-1], ['[on green] p [/]', ' r ', '[on green] o [/]', '[on yellow] o [/]', ' f '])

    def test_update_result(self):
        #Test that update result method applies correct _result attribute
        self.game._update_result(True, 3)
        self.assertEqual(self.game._result, {'won': True, 'rounds': '3'})

    def test_reset(self):
        #Setup game values matching a completed game
        self.game._result = {'won': True, 'rounds': '2'}
        self.game._solution = 'pooch'
        self.game._guesses = [[' a ', ' b ', ' c ', ' d ', ' e '], [' a ', ' b ', ' c ', ' d ', ' e '], [' a ', ' b ', ' c ', ' d ', ' e ']]
        #Call reset method
        self.game.reset()
        #Test that attributes are reset
        self.assertIsNone(self.game._result)
        self.assertIsNone(self.game._solution)
        self.assertEqual(self.game._guesses, [])

    def test_get_result(self):
        #Test get result method returns the value of _result attribute
        self.game._result = {'won': False, 'rounds': '3'}
        self.assertEqual(self.game.get_result(), {'won': False, 'rounds': '3'})

    def test_use_word_classmethod(self):
        #Create new game object to test alternate constructor
        test_game = WordGame.use_word('apple')
        #Test that game object has chosen solution
        self.assertEqual(test_game._solution, 'apple')
        #Test that object is only returned if word is 5 chars
        self.assertIsNone(WordGame.use_word('apples'))
        self.assertIsNone(WordGame.use_word('app'))

if __name__ == '__main__':
    unittest.main()
