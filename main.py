from rich import print
from rich_pyfiglet import RichFiglet

from include.session import Session
from include.game import WordGame
from include.menu import Menu
from include.settings import FILEPATH_USERLIB

def main():
    #Load session & game objects
    session = Session(user_filepath=FILEPATH_USERLIB)
    game = WordGame()

    #First show a welcome message
    banner = RichFiglet("Word Guesser", font='ansi_shadow', colors=["green", "yellow"])
    print('\n',banner,'\n')

    print('[yellow]Choose an option from the menu below. Simply type the option number (e.g. 1)[/yellow]')
    #Build main terminal menus 
    main_menu_options = {
        'Login': session.login,
        'Create new user':session.create_new_user,
        'Exit': None
    }

    loggedin_menu_options = {
        'Play new game': game.play_game,
        'How to play': game.get_instructions,
        'View my scores': session.print_scores,
        'Logout': session.logout,
        'Exit': None
    }

    main_menu = Menu(main_menu_options)
    submenu = Menu(loggedin_menu_options)

    #Main loop
    while True:
        #Check if user currently logged in to determine which menu to display
        if session.logged_in_user is None:
            exit_code = main_menu.run()
            #Menu.run() will return 'exit' if user wants to leave (selected menu option is None)
            #In this case exit main loop & terminate app
            if exit_code == 'exit': break
        else:
            #If user logged in - check if the game object has a result
            game_result = game.get_result()
            if game_result is not None:
                #If there's a game result, log scores & reset the game to be played again
                session.update_scores(game_result)
                game.reset()
            #Show logged in user menu options
            print(f"\n👋  [green]Hi, [bold]{session.logged_in_user}![/bold] What do you want to do?[/]\n")
            #Menu.run() returns 'continue' by default, unless user wants to exit
            exit_code = submenu.run()
            if exit_code == 'exit': break
            if exit_code == 'continue': continue

    print('[yellow]Thanks for playing! See you next time[/]\n')
    exit_banner = RichFiglet("Bye!", font='ansi_shadow', colors=["green", "yellow"])
    print(exit_banner)

#Run the app
if __name__ == '__main__':
    main()