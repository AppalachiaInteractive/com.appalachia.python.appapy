import argparse
from colorama import Fore, Back, Style

print(f'{Style.DIM}----- {Style.RESET_ALL}{Style.BRIGHT}{Fore.BLUE}Appalachia Interactive {Fore.GREEN}: {Fore.YELLOW}Appa{Fore.CYAN}Py{Style.DIM}{Fore.WHITE} -----{Style.RESET_ALL} ')

parser = argparse.ArgumentParser(description="Appalachia Interaactive - Enter your arguments...")

parser.add_argument(
    "command", metavar="[COMMAND]", type=str, help="The command to execute."
)

parser.add_argument(
    "subargs",
    metavar="[SUBARGS]",
    type=str,
    nargs="*",
    help="The subcommand or additional args for the command.",
)

args = parser.parse_args()

if args.command == 'templating':
    from appapy.templating import main
    main.execute(args.subargs)
elif args.command == 'packaging':
    from appapy.packaging import main
    main.execute(args.subargs)
elif args.command == 'publish':
    from appapy.packaging import publish
    publish.execute(args.subargs)
else:
    raise ValueError(args.command)



