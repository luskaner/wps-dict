from . import mac
from netaddr import EUI
import argparse

eui_format_help_url = 'https://pythonhosted.org/netaddr/tutorial_02.html#formatting'


def _bssid(mac_str: str) -> EUI:
    mac_converted = mac.mac(mac_str)
    if mac_converted:
        return mac_converted
    else:
        raise argparse.ArgumentTypeError(
            'BSSID format is incorrect (see {} for supported formats)'.format(eui_format_help_url))


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--version', action='store_true')
    subparsers = parser.add_subparsers(dest='action')
    gen_parser = subparsers.add_parser('generate', formatter_class=argparse.RawTextHelpFormatter)
    gen_parser.add_argument('bssid', type=_bssid,
                            help='BSSID in MAC address format\n(see {} for supported formats)'.format(
                                eui_format_help_url))
    gen_parser.add_argument('-e', '--essid', type=str)
    gen_parser.add_argument('-s', '--serial', type=str)
    gen_parser.add_argument('-a', '--all', action='store_true', help='Generates the dictionary using all the available algorithms')

    subparsers.add_parser('update_db')

    return parser.parse_args()
