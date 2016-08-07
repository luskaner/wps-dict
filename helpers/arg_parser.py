from . import mac
from netaddr import EUI
import argparse
from tools.core.helper import *
from providers.offline.core.helper import *
from providers.online.core.helper import *
from providers.online.downloadable.core.helper import *

eui_format_help_url = 'https://pythonhosted.org/netaddr/tutorial_02.html#formatting'
tools_names = list(tools.keys())
providers_names = list(offline_providers)
providers_names.extend(online_providers)
providers_names.extend(online_downloadable_providers)


def _bssid(mac_str: str) -> EUI:
    mac_converted = mac.mac(mac_str)
    if mac_converted:
        return mac_converted
    else:
        raise argparse.ArgumentTypeError(
            'BSSID format is incorrect (see {} for supported formats)'.format(eui_format_help_url))


class ToolsListAction(argparse.Action):
    CHOICES = ['smart', 'all']
    CHOICES.extend(tools_names)

    def __call__(self, parser, namespace, values, option_string=None):
        if values:
            if ('smart' in values and len(values) > 1) or ('all' in values and len(values) > 1):
                message = 'The "smart" or "all" values have to be the single choice'
                raise argparse.ArgumentError(self, message)
            for value in values:
                if value not in self.CHOICES:
                    message = ("Invalid tool: {0!r} (choose from {1})"
                               .format(value,
                                       ', '.join([repr(action)
                                                  for action in self.CHOICES])))

                    raise argparse.ArgumentError(self, message)
            setattr(namespace, self.dest, values)


class ProviderListAction(argparse.Action):
    CHOICES = ['all', 'none']
    CHOICES.extend(providers_names)

    def __call__(self, parser, namespace, values, option_string=None):
        if values:
            if ('none' in values and len(values) > 1) or ('all' in values and len(values) > 1):
                message = 'The "none" or "all" values have to be the single choice'
                raise argparse.ArgumentError(self, message)
            for value in values:
                if value not in self.CHOICES:
                    message = ("Invalid provider: {0!r} (choose from {1})"
                               .format(value,
                                       ', '.join([repr(action)
                                                  for action in self.CHOICES])))

                    raise argparse.ArgumentError(self, message)
            setattr(namespace, self.dest, values)


def parse():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='action')
    gen_parser = subparsers.add_parser('generate', formatter_class=argparse.RawTextHelpFormatter)
    gen_parser.add_argument('bssid', type=_bssid,
                            help='BSSID in MAC address format\n(see {} for supported formats)'.format(
                                eui_format_help_url))
    gen_parser.add_argument('-e', '--essid', type=str)
    gen_parser.add_argument('-s', '--serial', type=str)
    gen_parser.add_argument('-t', '--tools', nargs='*', action=ToolsListAction,
                            default=['smart'], help=(
            'Specify the tool(s) to generate from or "all" to run them all:\nAvailable tools: {}\nDefault: "smart" (chooses the tools to run depending on the bssid, essid and serial)'.format(
                ', '.join(tools_names))))
    gen_parser.add_argument('-p', '--providers', nargs='*', action=ProviderListAction,
                            default=['all'], help=(
            'Specify the provider(s) to get the pins or info from or, "none" to not use providers, or\n"all" to use them all:\nAvailable providers: {}\nDefault: "all"'.format(
                ', '.join(providers_names))))
    subparsers.add_parser('update_db')

    return parser.parse_args()
