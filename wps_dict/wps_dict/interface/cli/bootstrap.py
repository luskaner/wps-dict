from colorama import init as colorama_init

from .arg_parser import parse
from ...actions.base import generate, update_db
from ...actions.cli import list_providers, list_tools


def init():
    colorama_init()
    args = parse()

    if args.action == 'list_providers':
        list_providers.go(args.csv)
    elif args.action == 'list_tools':
        list_tools.go(args.csv)
    elif args.action == 'generate':
        if 'auto' in args.include_tools and 'auto' in args.exclude_tools:
            auto_mode = True
        else:
            auto_mode = False

        if 'none' in args.include_providers or 'all' in args.exclude_providers:
            no_providers = True
        else:
            no_providers = False

        if 'none' in args.include_tools or 'all' in args.exclude_tools:
            no_tools = True
        else:
            no_tools = False

        if auto_mode and no_providers:
            print('\033[1m\033[31mTo use the smart mode on the tools you have to select at least 1 provider\033[0m')
            exit(2)
        elif no_tools and no_providers:
            print('\033[1m\033[31mYou have to select at least 1 provider or tool\033[0m')
            exit(2)
        else:
            if not args.essid:
                args.essid = ''
            if not args.serial:
                args.serial = ''
            res, error_code = generate.go(
                args.bssid,
                args.essid,
                args.serial,
                args.include_tools,
                args.exclude_tools,
                args.include_providers,
                args.exclude_providers
            )
            if args.csv:
                print('pin')
                print('\n'.join(res))
            else:
                if error_code == 3:
                    print('\033[1m\033[33mWARNING: Online providers are checked without internet connection\033[0m')
                print('The resulting pin(s) is/are:\n\033[1m\033[32m{0}\033[0m'.format(
                    ', '.join(res))
                )
            exit(error_code)
    elif args.action == 'update_db':
        error_code = update_db.go(args.include_providers, args.exclude_providers)
        if error_code == 3 and not args.csv:
            print('\033[1m\033[33mWARNING: Only offline databases are updated without internet connection\033[0m')
        exit(error_code)
