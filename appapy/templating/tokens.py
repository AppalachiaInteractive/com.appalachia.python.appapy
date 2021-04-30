from typing import Callable


class TokenizedProperty:
    def __init__(self, key: str, display_name: str, enter_message: str, confirmation_message:str, enter_validation: Callable):
        self.key = key
        self.display_name = display_name
        self.value = ""
        self.enter_message = enter_message
        self.confirmation_message = confirmation_message
        self.enter_validation = enter_validation

    def set(self, value: str):
        self.value = value

    def replace(self, line: str) -> str:
        old = f"!!{self.key}!!"
        new = self.value
        line = line.replace(old, new)
        return line
