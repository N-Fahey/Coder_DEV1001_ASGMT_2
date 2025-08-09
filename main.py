from include.session import Session
from include.game import WordGame
from include.menu import Menu
from include.settings import FILEPATH_USERLIB

def main():
    #Load session & game objects
    session = Session(user_filepath=FILEPATH_USERLIB)
    game = WordGame()

    #First show a welcome message - TEMP
    print('--- Welcome To Game This text will be stylised ---')

    loggedin_menu_options = {
        'Play new game': game.play_game,
        'View my scores': session.print_scores,
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

if __name__ == '__main__':
    main()