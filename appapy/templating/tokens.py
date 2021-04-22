class TokenizedProperty:
    def __init__(self, key: str, display_name: str, message: str):
        self.key = key
        self.display_name = display_name
        self.value = ""
        self.message = message

    def set(self, value: str):
        self.value = value

    def replace(self, line: str) -> str:
        old = f"!!{self.key}!!"
        new = self.value
        line = line.replace(old, new)
        return line