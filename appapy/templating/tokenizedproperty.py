from typing import Callable

from colorama.ansi import Fore


class TokenizedProperty:
    def __init__(self, key: str, display_name: str, enter_validation: Callable):
        self.key = key
        self.display_name = display_name
        self.value = ""
        self.enter_message = f"Enter the {display_name.lower()} of the package"
        self.selection_message = f"Select the {display_name.lower()} of the package"
        self.confirmation_message = (
            f"Is this the intended {display_name.lower()} of the package?  {Fore.CYAN}[{{0}}]"
        )
        self.enter_validation = enter_validation

    def set(self, value: str):
        self.value = value

    def replace(self, line: str) -> str:
        old = f"!!{self.key}!!"
        new = self.value
        line = line.replace(old, new)
        return line

    def ispresent(self, line:str) -> bool:
        return f"!!{self.key}!!" in line
