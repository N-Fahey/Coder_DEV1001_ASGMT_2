import random
from rich.table import Table
from rich import print

from .settings import FILEPATH_WORDLIST

class Game():
    def __init__(self, game_type):
        '''General game class'''
        self._game_type = game_type
        self._result = None

class WordGame(Game):
    def __init__(self):
        '''Word game class'''
        super().__init__('WordGame')
        self._wordlist = self._get_wordlist()
        self._solution = None
        self._guesses = []

    def _get_wordlist(self) -> list:
        '''Get a list of valid words from a file system. Expects one word per line
            Returns: list'''
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
        '''Set the solution to a randomly chosen word from the wordlist'''
        #Ensure word list has been loaded
        if self._wordlist is None:
            raise AttributeError("No wordlist loaded")
        
        #Assign chosen word as the solution
        self._solution = random.choice(self._wordlist)
    
    def _check_guess(self, guess:str):
        '''Checks the provided guess against the solution.
            Returns: bool'''

        guess_formatted = []
        
        #Loop through letters in the guess
        for i, letter in enumerate(guess):
            if self._solution[i] == letter:
                # The letter is in the same spot as the solution, add with green background to formatted string
                guess_formatted.append(f'[on green] {letter} [/]')
                continue
            if letter in self._solution:
                #The letter is in the word, but wrong spot, add with yellow background
                guess_formatted.append(f'[on yellow] {letter} [/]')
                continue
            #Letter wasn't in solution, so add without formatting
            guess_formatted.append(f' {letter} ')

        #Record the guess    
        self._guesses.append(guess_formatted)

        #Check if the guess was the solution
        if guess.lower() == self._solution:
            return True
        
        return False
    
    def _update_result(self, won:bool, round_no:int = None):
        '''Update the saved result attribute with current games result'''
        self._result = {
            'won': won,
            'rounds': str(round_no)
        }

    def get_instructions(self):
        '''Print the game instructions'''
        instructions = Table()
        instructions.add_column("Guess the 5 letter word!", justify='center')
        instructions.add_row("Type any 5 letter word")
        instructions.add_row("Green letters are correct")
        instructions.add_row("Yellow letters are in the word, but wrong spot")
        instructions.add_row("You have 6 guesses. Good luck!")
        print(instructions)

    def reset(self):
        '''Reset the game attributes'''
        self._choose_random_word()
        self._result = None
        self._guesses = []

    def get_result(self) -> dict:
        '''Get results for the current game
            Returns: dict'''
        return self._result

    def play_game(self):
        '''Method to run the game'''
        #Select a random word from loaded word list
        self._choose_random_word()
        self.get_instructions()
        #Loop through number of guesses (6)
        for num in range(1,7):
            print(f'Guess {num}/6')
            #Prompt user for their guess, accepting guesses that are in the wordlist only
            while True:
                guess = input('>>> ').lower()
                if guess in self._wordlist:
                    break
            
            #Check the guess
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
        print(f"🙁  Sorry, you didnt get this one. The word was [green]{self._solution}[/].")
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