from include.login import UserLibrary
from include.game import WordGame
from include.menu import Menu
from include.settings import FILEPATH_USERLIB, USERNAME_MIN_LENGTH, PASSWORD_MIN_LENGTH

def placeholder():
    pass

def check_settings():
    pass

def main():
    #Load userlib
    userlib = UserLibrary(filepath=FILEPATH_USERLIB)
    #First show a welcome message

    #tmp
    game = WordGame()
    print('--- Welcome To Game This text will be stylised ---')

    loggedin_menu_options = {
        'Play new game': game.random_word,
        'View game history': placeholder,
        'View high scores': placeholder,
        'Logout': userlib.logout,
        'Exit': None
    }

    main_menu_options = {
        'Login': userlib.login,
        'Create new user':userlib.create_new_user,
        'Exit': None
    }
    main_menu = Menu(main_menu_options)
    submenu = Menu(loggedin_menu_options)
    while True:
        if userlib.logged_in_user is None:
            exit_code = main_menu.run()
            if exit_code == 'exit': break
        else:
            print(f"Welcome back, {userlib.logged_in_user}!")
            exit_code = submenu.run()
            if exit_code == 'exit': break
            if exit_code == 'continue':continue
        

    ### Login Stage ###
    #Check if any users, if none skip to user creation
    #Login

    #Create user

    #Exit

    ### Game Stage ###
    #If want to play, choose random word / specific word
    #Other options - check user score history, leaderboards, logout, exit

    #Game - random / specific word

    ## Other Options ##
    #Check user scores

    #Check leaderboards

    #Logout

    #Exit (and logout)

if __name__ == '__main__':
    main()