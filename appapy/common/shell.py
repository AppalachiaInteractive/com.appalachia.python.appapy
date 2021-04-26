import subprocess

from colorama import Fore


def run(command: str):
    print(f"{Fore.CYAN}Executing: {Fore.YELLOW}[{command}]{Fore.RESET}")
    subprocess.run(command, shell=True, check=True)

def run_and_read(command: str) -> str:
    print(f"{Fore.CYAN}Executing: {Fore.YELLOW}[{command}]{Fore.RESET}")
    p = subprocess.run(command, shell=True, check=True,stdout=subprocess.PIPE)
    return p.stdout.strip()