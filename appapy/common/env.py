import os

def get_home() -> str:
    home = os.getenv("HOME")
    return home

def get(param : str) -> str:
    val = os.getenv(param)
    return val

