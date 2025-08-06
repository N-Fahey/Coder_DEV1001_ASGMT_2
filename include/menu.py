from types import FunctionType, MethodType

class Menu():
    def __init__(self, options:dict):
        '''Class for menu functionality.
        Expects options dictionary in format {option string:function}'''
        menu_strings = []
        menu_actions = {}
        for  number, (option, func) in enumerate(options.items()):
            menu_strings.append(f"{number + 1}: {option}")
            menu_actions[number + 1] = func
        
        self._menu_string = '\n'.join(menu_strings)
        self._menu_actions = menu_actions
    
    def _show_options(self):
        print(self._menu_string)
    
    def _get_input(self):
        while True:
            user_selection = input(">>> ")
            try:
                user_selection = int(user_selection)
                return user_selection
            except ValueError:
                continue
    
    def _run_action(self, selection):
        if selection not in self._menu_actions.keys():
            raise KeyError(f"Menu option {selection} doesn't exist")
        
        action = self._menu_actions[selection]
        if action is None:
            return 'exit'

        if type(action) not in [FunctionType, MethodType]:
            raise TypeError("Menu selection is not a function")        
        
        self._menu_actions[selection]()
        return 'continue'
    
    def run(self):
        self.active = True
        while True:
            self._show_options()
            user_selection = self._get_input()
            if user_selection not in self._menu_actions.keys():
                continue
            run = self._run_action(user_selection)
            if run in ['exit', 'continue']:
                return run

