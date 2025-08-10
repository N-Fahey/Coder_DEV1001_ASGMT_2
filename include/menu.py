from types import FunctionType, MethodType
from rich import print

class Menu():
    def __init__(self, options:dict):
        '''Class for menu functionality.
        Expects options dictionary in format {option string:function}'''
        menu_strings = []
        menu_actions = {}
        for  number, (option, func) in enumerate(options.items()):
            menu_strings.append(f"  {number + 1}: {option}")
            menu_actions[number + 1] = func
        
        self._menu_string = '\n'.join(menu_strings)
        self._menu_actions = menu_actions
    
    def _show_options(self):
        '''Prints the menu options'''
        print(self._menu_string)
    
    def _get_input(self):
        '''Prompt user to select menu option'''
        while True:
            user_selection = input(">>> ")
            try:
                user_selection = int(user_selection)
                return user_selection
            except ValueError:
                continue
    
    def _run_action(self, selection):
        '''Calls the option for provided menu selection
            Returns:str (exit code)'''
        if selection not in self._menu_actions:
            raise KeyError(f"Menu option {selection} doesn't exist")
        
        #Get the action for provided menu option. If option is None, return exit code 'exit'
        action = self._menu_actions[selection]
        if action is None:
            return 'exit'

        #Check selection action is callable
        if type(action) not in [FunctionType, MethodType]:
            raise TypeError("Menu selection is not a function")        
        
        #Call the action, then return exit code 'continue'
        self._menu_actions[selection]()
        return 'continue'
    
    def run(self):
        '''Method to run the menu & get user selection'''
        #Loop menu while active
        while True:
            self._show_options()
            user_selection = self._get_input()
            if user_selection not in self._menu_actions.keys():
                continue
            run = self._run_action(user_selection)
            if run in ['exit', 'continue']:
                return run

