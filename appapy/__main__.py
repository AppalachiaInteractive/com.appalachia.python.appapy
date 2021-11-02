import argparse
import os

from colorama import Back, Fore, Style

from appapy.common.cli import note

# os.environ["APPA_FAST"] = "1"

print(f'{Style.DIM}----- {Style.RESET_ALL}{Style.BRIGHT}{Fore.BLUE}Appalachia Interactive {Fore.GREEN}: {Fore.YELLOW}Appa{Fore.CYAN}Py{Style.DIM}{Fore.WHITE} -----{Style.RESET_ALL} ')

parser = argparse.ArgumentParser(description="Appalachia Interactive - Enter your arguments...")

parser.add_argument(
    "command", metavar="COMMAND", type=str, help="The command to execute."
)

parser.add_argument(
    "subargs",
    metavar="SUBARGS",
    type=str,
    nargs="*",
    help="The subcommand or additional args for the command.",
)

args = parser.parse_args()

note(args)

if args.command == 'templating':
    from appapy.templating import main
    main.execute(args.subargs)
elif args.command == 'templating.json':
    from appapy.templating.json import main
    main.execute(args.subargs)
elif args.command == 'data':
    from appapy.data import main
    main.execute(args.subargs)
elif args.command == 'packaging':
    from appapy.packaging import main
    main.execute(args.subargs)
elif args.command == 'version':
    from appapy.packaging import version
    version.execute(args.subargs)
elif args.command == 'package':
    from appapy.packaging import publish
    publish.execute(args.subargs, False)
elif args.command == 'publish':
    from appapy.packaging import publish
    publish.execute(args.subargs, True)
elif args.command == 'imaging':
    from appapy.imaging import main
    main.execute(args.subargs)
else:
    parser.print_help()
    raise ValueError(args.command)



