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


class IncludeToolAction(argparse.Action):
    CHOICES = ['smart', 'all', 'none']
    CHOICES.extend(tools_names)

    def __call__(self, parser, namespace, values, option_string=None):
        if values:
            if len(values) == len(self.CHOICES) - 3:
                self.CHOICES = ['smart']
            if ('all' in values and len(values) > 1) or (
                ('none' in values and len(values) > 1) or ('smart' in values and len(values) > 1)):
                message = 'The "none", "all", "smart" values have to be the single choice'
                raise argparse.ArgumentError(self, message)
            for value in values:
                if value not in self.CHOICES:
                    message = ("Invalid tool(s) included: {0!r} (choose from {1})"
                               .format(value,
                                       ', '.join([repr(action)
                                                  for action in self.CHOICES])))

                    raise argparse.ArgumentError(self, message)
            setattr(namespace, self.dest, values)


class ExcludeToolAction(argparse.Action):
    CHOICES = ['smart', 'all']
    CHOICES.extend(tools_names)

    def __call__(self, parser, namespace, values, option_string=None):
        if values:
            if ('none' in values and len(values) > 1) or ('smart' in values and len(values) > 1):
                message = 'The "none" and "smart" values have to be the single choice'
                raise argparse.ArgumentError(self, message)
            for value in values:
                if value not in self.CHOICES:
                    message = ("Invalid tool(s) excluded: {0!r} (choose from {1})"
                               .format(value,
                                       ', '.join([repr(action)
                                                  for action in self.CHOICES])))

                    raise argparse.ArgumentError(self, message)
            setattr(namespace, self.dest, values)


class IncludeProviderAction(argparse.Action):
    CHOICES = ['none']
    CHOICES.extend(providers_names)

    def __call__(self, parser, namespace, values, option_string=None):
        if values:
            if 'none' in values and len(values) > 1:
                message = 'The "none" value have to be the single choice'
                raise argparse.ArgumentError(self, message)
            for value in values:
                if value not in self.CHOICES:
                    message = ("Invalid provider(s) included: {0!r} (choose from {1})"
                               .format(value,
                                       ', '.join([repr(action)
                                                  for action in self.CHOICES])))

                    raise argparse.ArgumentError(self, message)
            setattr(namespace, self.dest, values)


class ExcludeProviderAction(argparse.Action):
    CHOICES = ['all']
    CHOICES.extend(providers_names)

    def __call__(self, parser, namespace, values, option_string=None):
        if values:
            if len(values) == len(self.CHOICES) - 1:
                self.CHOICES = ['all']
            if 'none' in values and len(values) > 1:
                message = 'The "all" value have to be the single choice'
                raise argparse.ArgumentError(self, message)
            for value in values:
                if value not in self.CHOICES:
                    message = ("Invalid provider(s) excluded: {0!r} (choose from {1})"
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
    tools_group = gen_parser.add_mutually_exclusive_group()
    tools_group.add_argument('--include-tools', nargs='*', action=IncludeToolAction,
                             help=(
                                 'Specify the tools(s) to generate the pins from or, "all" to use all tools:\nAvailable tools: {}\nDefault: "smart" (chooses the tools to include depending on the bssid, essid and serial)'.format(
                                     ', '.join(tools_names))), metavar='TOOL', default='smart')
    tools_group.add_argument('--exclude-tools', nargs='*', action=ExcludeToolAction,
                             help=(
                                 'Specify the tools(s) to exclude generating the pins from or, "none" to use all tools::\nAvailable tools: {}\nDefault: "smart" (chooses the tools to exclude depending on the bssid, essid and serial)'.format(
                                     ', '.join(tools_names))), metavar='TOOL', default='smart')
    providers = gen_parser.add_mutually_exclusive_group()
    providers.add_argument('--include-providers', nargs='*', action=IncludeProviderAction,
                           help=(
                               'Specify the provider(s) to get the pins or info from or, "none" to not use providers:\nAvailable providers: {}\nDefault: "all"'.format(
                                   ', '.join(providers_names))), metavar='PROVIDER', default='all')
    providers.add_argument('--exclude-providers', nargs='*', action=ExcludeProviderAction,
                           help=(
                               'Specify the provider(s) to NOT get the pins or info from or, "all" to not use any provider:\nAvailable providers: {}\nDefault: "none"'.format(
                                   ', '.join(providers_names))), metavar='PROVIDER', default='none')
    subparsers.add_parser('update_db')

    return parser.parse_args()
