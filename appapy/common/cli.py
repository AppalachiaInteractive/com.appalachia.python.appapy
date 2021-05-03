

from typing import Callable, List

from colorama import Fore, Style

from appapy.common.exceptions import QuitError, RestartError


def demarcate(message):
    print(f"{Style.NORMAL}{Fore.LIGHTBLACK_EX}-------------------------------------{Style.RESET_ALL}")
    print(f"{Style.NORMAL}{Fore.LIGHTBLACK_EX}| {Style.BRIGHT}{Fore.LIGHTYELLOW_EX}{message}{Style.RESET_ALL}")
    print(f"{Style.NORMAL}{Fore.LIGHTBLACK_EX}-------------------------------------{Style.RESET_ALL}")
    
def note(message):
    print(f"{Style.NORMAL}{Fore.CYAN}{message}{Style.RESET_ALL}")
    
def highlight(prefix, message):
    print(f"{Style.BRIGHT}{Fore.CYAN}{prefix}: [{message}]{Style.RESET_ALL}")
    
def celebrate(message):
    print(f"{Style.BRIGHT}{Fore.GREEN}{message}{Style.RESET_ALL}")
          
    
def should_quit(parameter: str) -> bool:
    if parameter == "":
        return False

    l = parameter.lower()

    if l == "q" or l == "x" or l == "exit" or l == "quit":
        return True
    return False

def should_restart(parameter: str) -> bool:
    if parameter == "":
        return False

    l = parameter.lower()

    if l == "r" or l == "restart":
        return True
    return False


def do_ask(message: str) -> bool:
    print()
    parameter = ""
    while True:
        parameter = input("{0}:  ".format(f"{Fore.YELLOW}{message}{Style.RESET_ALL}")).strip()

        if parameter == "":
            continue

        l = parameter.lower()
        if l == "y" or l == "1" or l == "t":
            return True
        if l == "n" or l == "0" or l == "f":
            return False

        if should_quit(parameter):
            raise QuitError(parameter)
        if should_restart(parameter):
            raise RestartError(parameter)


def do_parameter(message: str, validation: Callable) -> str:
    print()
    parameter = ""
    while True:
        parameter = input("{0}:  ".format(f"{Fore.YELLOW}{message}{Style.RESET_ALL}")).strip()

        if should_quit(parameter):
            raise QuitError(parameter)
        if should_restart(parameter):
            raise RestartError(parameter)

        if validation(parameter):
            break

    return parameter


def do_selection(options: List[object], message: str) -> int:
    print()
    mini, maxi = 1, len(options)
    while True:
        for index, option in enumerate(options):
            print(f"{Fore.GREEN}[{index + 1}]: {Fore.CYAN}{option}{Style.RESET_ALL}")

        parameter = input("{0}:  ".format(f"{Fore.YELLOW}{message}{Style.RESET_ALL}")).strip()

        if should_quit(parameter):
            raise QuitError(parameter)
        if should_restart(parameter):
            raise RestartError(parameter)

        try:
            parameter_int = int(parameter)

            assert parameter_int >= mini and parameter_int <= maxi
            parameter_int = parameter_int - 1
            return parameter_int

        except Exception as e:
            print(f"{Fore.RED}Try again...{Style.RESET_ALL}")


def do_ask_until_confirmed(
    initial_value: str,
    confirmation_message: str,
    enter_message: str,
    enter_validation: Callable,
) -> str:
    confirmation = False
    value = initial_value
    while not confirmation:
        confirmation = do_ask(confirmation_message.format(value))
        if not confirmation:
            value = do_parameter(enter_message, enter_validation)

    return value


def do_selection_until_confirmed(
    confirmation_message: str, selection_options: List[object], selection_message: str
) -> int:
    confirmation = False
    opts=[o.name for o in selection_options]
    value = do_selection(opts, selection_message)
    while not confirmation:
        option = selection_options[value]
        if hasattr(option, "name") and hasattr(option, "notes"):
            print(f"{Fore.CYAN}[{option.name}]  {Fore.BLUE}{option.notes}{Style.RESET_ALL}")
        elif hasattr(option, "name"):
            print(f"{Fore.CYAN}{option.name}{Style.RESET_ALL}")
        elif hasattr(option, "notes"):
            print(f"{Fore.BLUE}{option.notes}{Style.RESET_ALL}")

        confirmation = do_ask(confirmation_message.format(option.name))

        if not confirmation:
            value = do_selection(opts, selection_message)

    return value

