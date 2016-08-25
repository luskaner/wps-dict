from netaddr import AddrFormatError, EUI, mac_bare
from copy import deepcopy


def from_oui_str(oui_str: str) -> EUI:
    try:
        sep_char = ''
        if ':' in oui_str:
            sep_char = ':'
        elif '-' in oui_str:
            sep_char = '-'
        return EUI("{}{sep}00{sep}00{sep}00".format(oui_str, sep=sep_char))
    except AddrFormatError:
        return None


def get_oui_from_eui(eui: EUI) -> str:
    mac_cp = deepcopy(eui)
    mac_cp.dialect = mac_bare
    return str(mac_cp)[0:6]


def get_ei_from_eui(eui: EUI) -> str:
    mac_cp = deepcopy(eui)
    return str(mac_cp.ei).replace('-', '')


def get_ei_int_from_eui(eui: EUI) -> str:
    return int(get_ei_from_eui(eui), 16)


def mac(mac_str: str) -> EUI:
    try:
        return EUI(mac_str)
    except AddrFormatError:
        return None
