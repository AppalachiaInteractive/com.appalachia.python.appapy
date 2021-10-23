import subprocess

from colorama import Fore


def run(command: str):
    print(f"{Fore.CYAN}Executing: {Fore.YELLOW}[{command}]{Fore.RESET}")
    subprocess.run(command, shell=True, check=True)

def run_and_read(command: str) -> str:
    print()
    print(f"{Fore.CYAN}Executing: {Fore.YELLOW}[{command}]{Fore.RESET}")
    p = subprocess.run(command, shell=True, check=True,stdout=subprocess.PIPE)
    out = str(p.stdout)
    clean = out.strip()
    args = [ "\\n", "\n", "b'", "'" ]    
    for i in range(2):
        clean = clean.strip()
        for arg in args:
            clean = clean.strip(arg)
    
    clean = clean.strip()
            
    print(f"{Fore.LIGHTBLUE_EX}OUT: {Fore.LIGHTCYAN_EX}[{out}]{Fore.RESET}")
    print(f"{Fore.LIGHTBLUE_EX}CLEAN: {Fore.LIGHTGREEN_EX}[{clean}]{Fore.RESET}")
    return clean