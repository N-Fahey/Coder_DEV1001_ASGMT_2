from include.login import UserLibrary


lib = UserLibrary('data/users.json')

user = input('Username: ')
password = input('Password: ')

if lib.check_login(user, password):
    print("Login success! Woohoo!")
else:
    print("Username or password is incorrect :(")