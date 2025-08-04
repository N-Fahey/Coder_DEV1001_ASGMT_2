from include.login import UserLibrary
from include.game import WordGame


lib = UserLibrary('data/userdata/users.json')

user = input('Username: ')
password = input('Password: ')

if lib.check_login(user, password):
    print("Login success! Woohoo!")
else:
    print("Username or password is incorrect :(")