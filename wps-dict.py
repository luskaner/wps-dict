#!/usr/bin/env python3

from helpers.arg_parser import *
import update_db
import generate

args = parse()
if args.action == 'update_db':
    update_db.go()
else:
    if not args.essid:
        args.essid = ''
    if not args.serial:
        args.serial = ''

    print(','.join(str(x) for x in generate.go(args.bssid, args.essid, args.serial, args.all)))
