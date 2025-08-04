import hashlib
import json
import os

#User class
class User():
    def __init__(self, username:str, hashed_password:str):
        '''Class to store user information (username, password & game stats)
        Will be instanciated by UserLib class when loading from file or adding a new user'''
        self._username = username
        self.__hashed_password = hashed_password
        self.games_played = 0
        self.games_won = 0
        self.scores = {
            1: 0,
            2: 0,
            3: 0,
            4: 0,
            5: 0,
            6: 0
        }
    
    def __repr__(self):
        return f"<User: '{self._username}'>"
    
    @staticmethod
    def hash_password(password:str):
        '''Take a plaintext password string and return sha256 hash of the string
        Returns: str'''
        password_encoded = password.encode('utf-8')
        hashed_password = hashlib.sha256(password_encoded).hexdigest()
        return hashed_password
    
    def export(self):
        '''Return a string representation of the user object, for saving to file
        Returns: str'''
        export_dict = {
            'username': self._username,
            'hash': self.__hashed_password,
            'played':self.games_played,
            'won':self.games_won,
            'scores':self.scores
        }
        print(export_dict)
        return export_dict

    def check_password(self, password:str):
        '''Check if provided plaintext password matches the saved password hash for the user
        Returns: bool'''
        password_hashed = self.hash_password(password)

        #If hashed version of provided password matches saved password, return True
        if password_hashed == self.__hashed_password:
            return True
        
        return False

class UserLibrary():
    def __init__(self, filepath:str):
        '''Class to load / store available user objects from users file'''
        self._users = {}
        self._filepath = filepath
        #Check filepath exists, otherwise create & log creation
        if not os.path.exists(filepath):
            print("Users file doesn't exist, creating it... ", end='')
            with open(filepath, 'x'):
                print("Success!")
        #Open file & load json into obj
        with open(filepath, 'r') as user_file:
            if len(user_file.read()) == 0:
                print('No users in userfile')
                return
            try:
                user_file.seek(0)
                user_json = json.load(user_file)
            except Exception as e:
                raise e

        #iterate & load users into _users
        for user in user_json:
            try:
                user_obj = User(user['username'], user['hash'])
                self._users[user['username']] = user_obj
            except Exception as e:
                raise e
    
    def user_exists(self, username:str):
        '''Check if provided username exists in saved UserLib
        Returns: bool'''
        if username in self._users.keys():
            return True
        
        return False

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
            with open(self._filepath, 'w') as user_file:
                json.dump(user_str_list, user_file, indent=4)
                return True
        except Exception as e:
            raise e

    def add_user(self, username:str, password:str):
        '''Create a new user
        Returns: bool (success/fail)'''
        if self.user_exists(username):
            raise ValueError('User already exists!')

        #Hash password to create user
        password_hashed = User.hash_password(password)

        #Create user obj
        new_user = User(username, password_hashed)

        #Update userlib file (call _ method)
        self._users[username] = new_user
        self._save_userfile()
        return True
    
    def check_login(self, username:str, password:str):
        '''Check if provided username & password correctly matches to a saved user'''
        if not self.user_exists(username):
            return False
        
        user = self._users[username]
        #Otherwise check password is correct using check_password method
        if not user.check_password(password):
            return False
        
        return True
