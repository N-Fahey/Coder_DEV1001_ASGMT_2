from include.session import Session
from include.game import WordGame
from include.menu import Menu
from include.settings import FILEPATH_USERLIB

def placeholder():
    pass

def check_settings():
    pass

def main():
    #Load session & game objects
    session = Session(user_filepath=FILEPATH_USERLIB)
    game = WordGame()

    #First show a welcome message - TEMP
    print('--- Welcome To Game This text will be stylised ---')

    loggedin_menu_options = {
        'Play new game': game.play_game,
        'View game history': placeholder,
        'View high scores': placeholder,
        'Logout': session.logout,
        'Exit': None
    }

    main_menu_options = {
        'Login': session.login,
        'Create new user':session.create_new_user,
        'Exit': None
    }
    main_menu = Menu(main_menu_options)
    submenu = Menu(loggedin_menu_options)

    while True:
        if session.logged_in_user is None:
            exit_code = main_menu.run()
            if exit_code == 'exit': break
        else:
            game_result = game.get_result()
            if game_result is not None:
                session.update_scores(game_result)
                game.reset()
            print(f"Welcome back, {session.logged_in_user}!")
            exit_code = submenu.run()
            if exit_code == 'exit': break
            if exit_code == 'continue': continue
        

    ### Login Stage ###
    #x Check if any users, if none skip to user creation
    #x Login

    #x Create user

    #x  Exit

    ### Game Stage ###
    #If want to play, choose random word / specific word
    #Other options - check user score history, leaderboards, logout, exit

    #x Game - random / specific word

    ## Other Options ##
    #Check user scores

    #Check leaderboards

    #x Logout

    #x Exit (and logout)

if __name__ == '__main__':
    main()