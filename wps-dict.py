#!/usr/bin/env python3

from helpers.arg_parser import *
import update_db
import generate

args = parse()
print(args)

if args.action == 'update_db':
    update_db.go(args.include_providers, args.exclude_providers)
else:
    if 'auto' in args.include_tools and 'smart' in args.exclude_tools:
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
        print('To use the smart mode you have to select at least 1 provider')
    elif no_tools and no_providers:
        print('You have to select at least 1 provider or tool')
    else:
        if not args.essid:
            args.essid = ''
        if not args.serial:
            args.serial = ''
        print(
            generate.go(
                args.bssid,
                args.essid,
                args.serial,
                args.include_tools,
                args.exclude_tools,
                args.include_providers,
                args.exclude_providers,
            )
        )
