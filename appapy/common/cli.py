

from shutil import Error
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

def parse_bool(message: str) -> bool:
    message = str(message)

    result = message.lower()
    
    if result == "y" or result == "1" or result == "t" or result == "true":
        return True
    if result == "n" or result == "0" or result == "f" or result == "false":
        return False  
            
    if should_quit(result):
        raise QuitError(result)

    if should_restart(result):
        raise RestartError(result)

    raise Error(message)
    
def do_ask(message: str, parameter: str) -> bool:
    print()
    
    while True:
        if parameter is not None:
            print("{0}:  {1}".format(f"{Fore.YELLOW}{message}{Style.RESET_ALL}", parameter))
        else:
            parameter = input("{0}:  ".format(f"{Fore.YELLOW}{message}{Style.RESET_ALL}")).strip()

        if parameter == "":
            parameter = None
            continue

        try:
            return parse_bool(parameter)
        except QuitError:
            raise            
        except RestartError:
            raise
        except:
            parameter = None
            continue 


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


def do_selection(options: List[object], message: str, parameter: int) -> int:
    print()
    mini, maxi = 1, len(options)
    auto = parameter is not None
    while True:

        for index, option in enumerate(options):
            print(f"{Fore.GREEN}[{index + 1}]: {Fore.CYAN}{option}{Style.RESET_ALL}")

        if (not auto):
            parameter = input("{0}:  ".format(f"{Fore.YELLOW}{message}{Style.RESET_ALL}")).strip()
            
            if should_quit(parameter):
                raise QuitError(parameter)
            if should_restart(parameter):
                raise RestartError(parameter)
        else:
            print("{0}:  {1}".format(f"{Fore.YELLOW}{message}{Style.RESET_ALL}", parameter))

        try:
            parameter_int = int(parameter)

            assert parameter_int >= mini and parameter_int <= maxi
            parameter_int = parameter_int - 1
            return parameter_int

        except Exception as e:
            parameter = None
            auto = False
            print(f"{Fore.RED}Try again...{Style.RESET_ALL}")


def do_ask_until_confirmed(
    initial_value: str,
    confirmation_message: str,
    enter_message: str,
    enter_validation: Callable,
    autoconfirm: bool
) -> str:

    value = initial_value

    if autoconfirm:
        do_ask(confirmation_message.format(value), "1")
        return value

    confirmation = None
    while not confirmation:
        confirmation = do_ask(confirmation_message.format(value), confirmation)
        if not confirmation:
            value = do_parameter(enter_message, enter_validation)
            confirmation = None

    return value


def do_selection_until_confirmed(
    confirmation_message: str, selection_options: List[object], selection_message: str, parameter: int
) -> int:
    autoconfirm = parameter != None
    confirmation = False
    opts=[o.name for o in selection_options]
    value = do_selection(opts, selection_message, parameter)

    if autoconfirm:        
        option = selection_options[value]
        do_ask(confirmation_message.format(option.name), "1")
        return value

    while not confirmation:
        option = selection_options[value]
        if hasattr(option, "name") and hasattr(option, "notes"):
            print(f"{Fore.CYAN}[{option.name}]  {Fore.BLUE}{option.notes}{Style.RESET_ALL}")
        elif hasattr(option, "name"):
            print(f"{Fore.CYAN}{option.name}{Style.RESET_ALL}")
        elif hasattr(option, "notes"):
            print(f"{Fore.BLUE}{option.notes}{Style.RESET_ALL}")

        confirmation = do_ask(confirmation_message.format(option.name), None)

        if not confirmation:
            value = do_selection(opts, selection_message, parameter)

    return value
