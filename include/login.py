import hashlib
import json
import os

#User class
class User():
    def __init__(self, username, hashed_password):
        self._username = username
        self.__hashed_password = hashed_password
    
    def __repr__(self):
        return f"<User: '{self._username}'>"
    
    @staticmethod
    def hash_password(password):
        #Hash password and return hash
        password_encoded = password.encode('utf-8')
        hashed_password = hashlib.sha256(password_encoded).hexdigest()
        return hashed_password
    
    def export(self):
        #Build json string / obj for save to file
        export_dict = {
            'Username': self._username,
            'Hash': self.__hashed_password
        }
        return export_dict

    def check_password(self, password):
        #Check provided hash against saved password
        password_hashed = self.hash_password(password)

        #If hashed version of provided password matches saved password, return True
        if password_hashed == self.__hashed_password:
            return True
        
        return False

class UserLibrary():
    def __init__(self, filepath):
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
                user_obj = User(user['Username'], user['Hash'])
                self._users[user['Username']] = user_obj
            except Exception as e:
                raise e
    
    def user_exists(self, username):
        #Check if provided username already exists (via attr)
        if username in self._users.keys():
            return True
        
        return False

    def _save_userfile(self):
        #Create list of users represented as JSON strings to save
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

    def add_user(self, username, password):
        #Check if username already exists (call method)
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
    
    def check_login(self, username, password):
        #If user doesn't exist, we know that login didn't work!
        if not self.user_exists(username):
            return False
        
        user = self._users[username]
        #Otherwise check password is correct using check_password method
        if not user.check_password(password):
            return False
        
        return True
