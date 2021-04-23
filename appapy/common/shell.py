import subprocess

from colorama import Fore


def run(command: str):
    print(f"{Fore.CYAN}Executing: {Fore.YELLOW}[{command}]{Fore.RESET}")
    subprocess.run(command, shell=True, check=True)
