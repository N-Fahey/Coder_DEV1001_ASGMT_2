import json
import getpass
import bcrypt
from num2words import num2words
from pathlib import Path
from rich.table import Table
from rich import print

from .settings import USERNAME_MIN_LENGTH, PASSWORD_MIN_LENGTH

#User class
class User():
    def __init__(self, username:str, hashed_password:str, played=0, won=0, scores=None):
        '''Class to store user information (username, password & game stats)
        Will be instantiated by Session class when loading from file or adding a new user'''

        self._username = username
        self.__hashed_password = hashed_password
        self.games_played = played
        self.games_won = won
        if scores is None:
            scores = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0}
        self.scores = scores
    
    def __str__(self):
        return f"{self._username}"
    
    def add_result(self, result:dict):
        '''Adds a game result to this User.
        Expects result = dict containing 'won'(bool), 'rounds'(int)'''

        if not {'won', 'rounds'}.issubset(result):
            raise KeyError('result dict expects keys: won, rounds')
        #Get required values
        won = result['won']
        rounds = result['rounds']

        #Increment games played regardless of result
        self.games_played += 1
        if won:
            #If won, increment both games won & the win count for this number of rounds
            self.games_won += 1
            self.scores[rounds] += 1
        
    
    @staticmethod
    def hash_password(password:str) -> bytes:
        '''Take a plaintext password string and return sha256 hash of the string
        Returns: bytes'''

        #Encode password string
        password_encoded = password.encode('utf-8')
        #Hash using bcrypt & return has as bytes
        hashed_password = bcrypt.hashpw(password_encoded, bcrypt.gensalt())
        return hashed_password
    
    def export(self) -> dict:
        '''Return a dict representation of the user object, for saving to file
        Returns: dict'''
        export_dict = {
            'username': self._username,
            'hash': self.__hashed_password.decode('utf-8'),
            'played':self.games_played,
            'won':self.games_won,
            'scores':self.scores
        }
        return export_dict

    def check_password(self, password:str) -> bool:
        '''Check if provided plaintext password matches the saved password hash for the user
        Returns: bool'''
        #OLD: password_hashed = self.hash_password(password)
        password_encoded = password.encode('utf-8')
        
        #If hashed version of provided password matches saved password, return True
        #OLD: if password_hashed == self.__hashed_password:
        if bcrypt.checkpw(password_encoded, self.__hashed_password):
            return True
        
        return False

class Session():
    def __init__(self, user_filepath:str):
        '''Class to manage users & current session state'''
        self._users = {}
        self._user_filepath = Path(user_filepath)
        self.logged_in_user = None

        #Check filepath exists, otherwise create it & any subdirs on the way
        if not self._user_filepath.exists():
            print("Users file doesn't exist, creating it... ", end='')
            self._user_filepath.parent.mkdir(exist_ok=True, parents=True)
            with open(self._user_filepath, 'w'):
                print("Success!")
        #Open file & load json into variable
        with open(self._user_filepath, 'r') as user_file:
            if len(user_file.read()) == 0:
                print('No users found in user file.')
                return
            try:
                user_file.seek(0)
                user_json = json.load(user_file)
            except json.JSONDecodeError as e:
                raise f'Unable to read user file, exiting: {e}'
            except Exception as e:
                raise f'Unexpected error while reading user file, exiting: {e}'

        #iterate & load users into _users
        for user in user_json:
            try:
                user_obj = User(username=user['username'], hashed_password=user['hash'].encode('utf-8'),
                                won=user['won'], played=user['played'], scores=user['scores'])
                self._users[user['username']] = user_obj
            except Exception as e:
                raise e

    def _save_userfile(self):
        '''Method to save current users from UserLib attribute to filesystem'''
        user_str_list = []

        #Iterate over user objects in self._users (dict values)
        for user in self._users.values():
            #Get user export string
            export_string = user.export()
            #Append to list
            user_str_list.append(export_string)
        
        try:
            with open(self._user_filepath, 'w') as user_file:
                json.dump(user_str_list, user_file, indent=4)
        except FileNotFoundError as e:
            print(f'Unable to load user file, has it been moved / deleted?. User details have not been saved: {e}')
        except Exception as e:
            print(f'Unexpected error when saving user details. User details have not been saved: {e}')

    def _add_user(self, username:str, password:str) -> User:
        '''Create a new user for the session & save new user information to user file
        Returns: User obj'''
        #Ensure user doesn't already exist
        if self.user_exists(username):
            raise ValueError(f'User {username} already exists!')

        #Hash the provided password using hash_password from the User class
        password_hashed = User.hash_password(password)

        #Create new user object
        new_user = User(username, password_hashed)

        #Add User object to loaded user list
        self._users[username] = new_user

        #Save user list to file
        self._save_userfile()
        return new_user
    
    def _check_login(self, username:str, password:str) -> bool:
        '''Check if provided username & password correctly matches to a saved user
            Returns: bool'''
        if not self.user_exists(username):
            return False
        
        user = self._users[username]
        #Otherwise check password is correct using check_password method
        if not user.check_password(password):
            return False
        
        return True
    
    def user_exists(self, username:str) -> bool:
        '''Check if provided username exists in saved UserLib
        Returns: bool'''
        return username in self._users

    def user_count(self) -> int:
        '''Get number of registered users
        Returns: int'''
        return len(self._users)
    
    def update_scores(self, result:dict):
        '''Update scores of the logged in user following game completion, and save updated details to user file'''

        self.logged_in_user.add_result(result)
        self._save_userfile()
    
    def print_scores(self):
        '''Print the game scores of the currently logged in user'''
        score_tbl = Table(show_edge=True)
        # Center align all columns
        score_tbl.add_column(header="[b]Your Scores[/b]", justify="center")
        score_tbl.add_row(f'[b]Games Played:[/b] {self.logged_in_user.games_played}')
        score_tbl.add_row(f'[b]Games Won:[/b] {self.logged_in_user.games_won}')
        for num in range(1, 7):
            score_tbl.add_row(f"[b]{num2words(num, to='ordinal_num')} guess:[/b] {self.logged_in_user.scores[str(num)]}")
        print(score_tbl)
    
    def create_new_user(self):
        '''Method to guide creation of a new user'''
        username = None
        password = None

        while username is None:
            username_input = input('Choose a username: ')

            #Check username length
            if len(username_input) < USERNAME_MIN_LENGTH:
                print(f'[red]Username needs to be {USERNAME_MIN_LENGTH} or more characters. Please try again...[/]')
                continue
            
            #Check if username already exists
            if self.user_exists(username_input):
                print(f'[red]User [bold]{username_input}[/bold] already exists. Please try again...[/]')
                continue

            #Confirm username
            username = username_input

        while password is None:
            password_input = getpass.getpass('Choose a password: ')

            #Check password length
            if len(password_input) < PASSWORD_MIN_LENGTH:
                print(f'[red]Password should be minimum {PASSWORD_MIN_LENGTH} characters. Please try again...[/]')
                continue

            #Confirm password
            password = password_input

        #Create the new user with provided details
        new_user = self._add_user(username, password)
        print(f"[green]User [bold]{new_user}[/bold] created! You can now log in[/]")
        return new_user
    
    def login(self):
        '''Method to allow user to attempt login'''
        #Get username / password
        username = input('Enter username: ')
        password = getpass.getpass('Enter password: ')

        #Check provided details
        result = self._check_login(username, password)

        #If details incorrect, advise
        if not result:
            print('[red]Login failed. Username & password not recognised[/]')
            return
        
        #Otherwise set user with provided username as the logged in user
        print(f'[green]Login successful![/]')
        self.logged_in_user = self._users[username]
    
    def logout(self):
        '''Method to log out the current user'''
        print(f'\n[green]See you later [bold]{self.logged_in_user}![/] 👋\n')
        self.logged_in_user = None
