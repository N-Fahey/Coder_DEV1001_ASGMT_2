from .settings import FILEPATH_WORDLIST
import random

from rich.table import Table
from rich import print

class Game():
    pass

class WordGame(Game):
    def __init__(self):
        self._wordlist = self._get_wordlist()
        self._solution = None
        self._guesses = []
        self._result = None

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
        
        self._solution = random.choice(self._wordlist)
    
    def _check_guess(self, guess:str):
        guess_formatted = []
        
        for i, letter in enumerate(guess):
            if self._solution[i] == letter:
                # The letter is in the same spot as the solution
                guess_formatted.append(f'[on green] {letter} [/]')
                continue
            if letter in self._solution:
                #The letter is in the word, but wrong spot
                guess_formatted.append(f'[on yellow] {letter} [/]')
                continue
            #Letter wasn't in solution
            guess_formatted.append(f' {letter} ')
            
        self._guesses.append(guess_formatted)

        if guess.lower() == self._solution:
            print('You got it! Woohoo!')
            return True
        
        return False
    
    def _update_result(self, won:bool, round_no:int = None):
        self._result = {
            'won': won,
            'rounds': round_no
        }

    def reset(self):
        self._choose_random_word()
        self._result = None
        self._guesses = []

    def get_result(self):
        return self._result

    def play_game(self):
        #Select a random word from loaded word list
        self._choose_random_word()
        print(self._solution)
        print('''
              *******************
              * GUESS THE WORD! *
              *******************''')
        for num in range(1,7):
            print(f'Guess {num}/6')
            while True:
                guess = input('>>> ')
                if guess in self._wordlist:
                    break
            
            result = self._check_guess(guess)
            #Create table grid to show results
            tbl = Table(show_header=False, show_lines=True)
            #Add 1 row for each guess
            for guess_formatted in self._guesses:
                tbl.add_row(*guess_formatted)
            #Top up to 6 total rows
            for _ in range(num,6):
                tbl.add_row()
            #Print the current table
            print(tbl)
            #Check if player won, after table so it still displays
            if result:
                print(f"🎉  Congrats, you won in {num} guesses! Yippee!")
                self._update_result(won=True, round_no=num)
                return
        #If execution gets here, didn't win
        print("🙁  Sorry, you didnt get this one.")
        self._update_result(won=False)

    @classmethod
    def random_word(cls):
        '''Alternate constructor to launch the game using a randomly chosen word from the loaded wordlist.
            If no wordlist, returns None
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
        '''Alternate constructor to launch the game using a selected word.
            Must be 5 characters
            Returns WordGame object'''
        word = input('Choose the word')
        if len(word) != 5:
            return None
        
        game_object = cls()

        #Assign the provided word
        game_object._solution = word

        return game_object