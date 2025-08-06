from .settings import FILEPATH_WORDLIST
import random

class Game():
    pass

class WordGame(Game):
    def __init__(self):
        self._wordlist = self._get_wordlist()
        self.solution = None

    def _get_wordlist(self):
        '''Get a list of valid words from a file system. Expects one word per line
            Returns: str'''
        try:
            with open(FILEPATH_WORDLIST) as word_file:
                #Read lines from word file and general a word list, without \n special chars
                word_list = [line.replace('\n','') for line in word_file.readlines()]
        except FileExistsError: 
            print("Word file doesn't exist. Unable to load word list")
            return None
        #Return to be applied to attribute
        return word_list
    
    def _choose_random_word(self):
        '''Return a randomly chosen word from the wordlist'''
        if self._wordlist is None:
            raise AttributeError("No wordlist loaded")
        
        self.solution = random.choice(self._wordlist)

    @classmethod
    def random_word(cls):
        '''Launch the game using a randomly chosen word from the loaded wordlist. If no wordlist, returns None
            Returns: WordGame object'''
        
        game_object = cls()

        if game_object._wordlist is None:
            return None
        
        #Choose a random word
        game_object._choose_random_word()

        #Return game object
        return game_object

    @classmethod
    def use_word(cls):
        '''Launch the game using a selected word. Must be 5 characters'''
        word = input('Choose the word')
        if len(word) != 5:
            return None
        
        game_object = cls()

        #Assign the provided word
        game_object.solution = word

        return game_object