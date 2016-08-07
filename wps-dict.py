#!/usr/bin/env python3

from helpers.arg_parser import *
import update_db
import generate

args = parse()
print(args)

if args.action == 'update_db':
    update_db.go()
else:
    if (args.providers and 'none' in args.providers) and (args.tools and 'smart' in args.tools):
        print('To use the smart mode in tools you have to select at least 1 provider')
    else:
        if not args.essid:
            args.essid = ''
        if not args.serial:
            args.serial = ''
        print(generate.go(args.bssid, args.essid, args.serial, args.tools, args.providers))
