import argparse
from sys import exit

from netaddr import EUI

from ...helpers import mac
from ...providers.offline.list import offline_providers
from ...providers.online.downloadable.list import online_downloadable_providers
from ...providers.online.queryable.list import online_queryable_providers
from ...tools.list import tools

eui_format_help_url = 'https://pythonhosted.org/netaddr/tutorial_02.html#formatting'
tools_names = list(tools.keys())
providers_names = list(offline_providers)
providers_names.extend(online_downloadable_providers)
updatable_providers_names = providers_names[:]
providers_names.extend(online_queryable_providers)


def _bssid(mac_str: str) -> EUI:
    mac_converted = mac.mac(mac_str)
    if mac_converted:
        return mac_converted
    else:
        raise argparse.ArgumentTypeError(
            '\033[1m\033[31mBSSID format is incorrect\033[39m \033[1m(see {} for supported formats)\033[0m'.format(
                eui_format_help_url))


class MultiChoiceAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None, label='option', choices=[], single_choices=[]):
        for single_choice in single_choices:
            if single_choice in values and len(values) > 1:
                message = '\033[1m\033[31mThe\033[39m \033[36m{0} \033[31mvalues have to be the single choice\033[0m'.format(
                    ', '.join([repr(action)
                               for action in
                               single_choices]))
                raise argparse.ArgumentError(self, message)
        if values:
            for value in values:
                if value not in choices:
                    message = (
                        "\033[1m\033[31mInvalid {0}(s):\033[39m \033[36m{1!r}\033[39m \033[0m(choose from\033[39m \033[36m{2}\033[39m\033[0m)"
                            .format(label, value,
                                    ', '.join([repr(action)
                                               for action in choices])))

                    raise argparse.ArgumentError(self, message)
            setattr(namespace, self.dest, values)


class IncludeToolAction(MultiChoiceAction):
    def __call__(self, parser, namespace, values, option_string=None):
        label = 'tool'
        choices = ['auto', 'all', 'none']
        single_choices = choices[:]
        choices.extend(tools_names)
        if len(values) == len(choices) - 3:
            choices = ['auto']
        super(IncludeToolAction, self).__call__(parser, namespace, values, option_string=None, label=label,
                                                choices=choices, single_choices=single_choices)


class ExcludeToolAction(MultiChoiceAction):
    def __call__(self, parser, namespace, values, option_string=None):
        label = 'tool'
        choices = ['auto', 'all', 'none']
        single_choices = choices[:]
        choices.extend(tools_names)
        super(ExcludeToolAction, self).__call__(parser, namespace, values, option_string=None, label=label,
                                                choices=choices, single_choices=single_choices)


class IncludeProviderAction(MultiChoiceAction):
    def __call__(self, parser, namespace, values, option_string=None):
        label = 'provider'
        choices = ['all', 'none']
        single_choices = choices[:]
        choices.extend(providers_names)
        super(IncludeProviderAction, self).__call__(parser, namespace, values, option_string=None, label=label,
                                                    choices=choices, single_choices=single_choices)


class ExcludeProviderAction(MultiChoiceAction):
    def __call__(self, parser, namespace, values, option_string=None):
        label = 'provider'
        choices = ['all', 'none']
        single_choices = choices[:]
        choices.extend(providers_names)
        if len(values) == len(choices) - 1:
            choices = ['all']
        super(ExcludeProviderAction, self).__call__(parser, namespace, values, option_string=None, label=label,
                                                    choices=choices, single_choices=single_choices)


class IncludeProviderUpdateDbAction(MultiChoiceAction):
    def __call__(self, parser, namespace, values, option_string=None):
        label = 'provider'
        choices = ['all']
        single_choices = choices[:]
        choices.extend(updatable_providers_names)
        super(IncludeProviderUpdateDbAction, self).__call__(parser, namespace, values, option_string=None, label=label,
                                                            choices=choices, single_choices=single_choices)


class ExcludeProviderUpdateDbAction(MultiChoiceAction):
    def __call__(self, parser, namespace, values, option_string=None):
        label = 'provider'
        choices = ['none']
        single_choices = choices[:]
        choices.extend(updatable_providers_names)
        super(ExcludeProviderUpdateDbAction, self).__call__(parser, namespace, values, option_string=None, label=label,
                                                            choices=choices, single_choices=single_choices)


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--csv', action='store_true',
                        help='Outputs in a CSV format instead of the standard human-readable output (except for errors and help)')
    subparsers = parser.add_subparsers(dest='action')
    subparsers.add_parser('list_providers', formatter_class=argparse.RawTextHelpFormatter)
    subparsers.add_parser('list_tools', formatter_class=argparse.RawTextHelpFormatter)
    gen_parser = subparsers.add_parser('generate', formatter_class=argparse.RawTextHelpFormatter)
    gen_parser.add_argument('bssid', type=_bssid,
                            help='BSSID in MAC address format\n(see {} for supported formats)'.format(
                                eui_format_help_url))
    gen_parser.add_argument('-e', '--essid', type=str)
    gen_parser.add_argument('-s', '--serial', type=str)
    tools_group = gen_parser.add_mutually_exclusive_group()
    tools_group.add_argument('--include-tools', nargs='*', action=IncludeToolAction,
                             help=(
                                 'Specify the tools(s) to generate the pins from, "all" to use all tools or, "none" to NOT\nuse any tools or "auto" to use them depending on the providers:\nAvailable tools: {}\nDefault: "smart" (chooses the tools to include depending on the bssid, essid and serial)'.format(
                                     ', '.join(tools_names))), metavar='TOOL', default='auto')
    tools_group.add_argument('--exclude-tools', nargs='*', action=ExcludeToolAction,
                             help=(
                                 'Specify the tools(s) to generate the pins from, "all" to NOT use any tools, "none" to use\nall tools or "auto" to use them depending on the providers\nAvailable tools: {}\nDefault: "smart" (chooses the tools to exclude depending on the bssid, essid and serial)'.format(
                                     ', '.join(tools_names))), metavar='TOOL', default='auto')
    providers = gen_parser.add_mutually_exclusive_group()
    providers.add_argument('--include-providers', nargs='*', action=IncludeProviderAction,
                           help=(
                               'Specify the provider(s) to get the info from, "all" to use them all or "none" to NOT any providers:\nAvailable providers: {}\nDefault: "all"'.format(
                                   ', '.join(providers_names))), metavar='PROVIDER', default='all')
    providers.add_argument('--exclude-providers', nargs='*', action=ExcludeProviderAction,
                           help=(
                               'Specify the provider(s) to NOT get the info from or, "all" to NOT use any provider or "none" to use them all:\nAvailable providers: {}\nDefault: "none"'.format(
                                   ', '.join(providers_names))), metavar='PROVIDER', default='none')
    update_db_parser = subparsers.add_parser('update_db', formatter_class=argparse.RawTextHelpFormatter)
    providers_update_db = update_db_parser.add_mutually_exclusive_group()
    providers_update_db.add_argument('--include-providers', nargs='*', action=IncludeProviderUpdateDbAction,
                                     help=(
                                         'Specify the provider(s) to get the info from or "all" to use them all:\nAvailable providers: {}\nDefault: "all"'.format(
                                             ', '.join(updatable_providers_names))), metavar='PROVIDER', default='all')
    providers_update_db.add_argument('--exclude-providers', nargs='*', action=ExcludeProviderUpdateDbAction,
                                     help=(
                                         'Specify the provider(s) to NOT get the info from or "none" to use them all:\nAvailable providers: {}\nDefault: "none"'.format(
                                             ', '.join(updatable_providers_names))), metavar='PROVIDER', default='none')

    args = parser.parse_args()
    if not args.action:
        parser.print_help()
        exit(2)
    else:
        return args
