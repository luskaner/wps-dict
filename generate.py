from netaddr import EUI
from os.path import dirname, abspath
import re
import os

from providers.core.results import *
from tools.core.helper import *
from providers.offline.core.helper import *
from providers.online.core.helper import *
from providers.online.downloadable.core.helper import *

providers_offline = offline_providers
providers_offline.update(online_downloadable_providers)


def _get_pins(res: ProviderResult, bssid: EUI, essid: str, serial: str) -> list:
    pins = set()
    oui_bssid = get_oui_from_eui(res.starting_mac)
    tools_run = set()

    if oui_bssid == get_oui_from_eui(bssid):
        pins.update(res.pins_sticker)
        pins.update(res.pins_user)
        for tool in res.tools:
            if tool in tools:
                pins.update(tools[tool].get_pins(bssid, essid, serial))
                tools_run.update([tool])

    for tool in tools:
        if not (tool in tools_run):
            if oui_bssid in tools[tool].supported_ouis():
                pins.update(tools[tool].get_pins(bssid, essid, serial))
            else:
                essids = tools[tool].supported_essids()
                serials = tools[tool].supported_serials()
                if essid and essids:
                    for e in essids:
                        if re.match(e, essid):
                            pins.update(tools[tool].get_pins(bssid, essid, serial))
                elif serial and serials:
                    for s in serials:
                        if re.match(s, serial):
                            pins.update(tools[tool].get_pins(bssid, essid, serial))
    return pins


def _read_all_db(bssid: EUI) -> ProviderResults:
    path = dirname(abspath(__file__)) + '/pins/'
    results = ProviderResults()

    for name, obj in providers_offline.items():
        with open(path + name + '.csv', newline='') as csv_file:
            pins_reader = csv.reader(csv_file)
            for _ in range(2):
                next(pins_reader)
            for row in pins_reader:
                res = ProviderResult.from_csv_array(row)
                results.add(res)

    for online_provider in online_providers.values():
        res = online_provider.load(bssid)
        if res:
            results.add(res)

    return results


def _read_db(bssid: EUI, providers_selected: list) -> ProviderResults:
    path = dirname(abspath(__file__)) + '/pins/'
    results = ProviderResults()

    for name, _ in providers_offline.items():
        if name in providers_selected:
            with open(path + name + '.csv', newline='') as csv_file:
                pins_reader = csv.reader(csv_file)
                for _ in range(2):
                    next(pins_reader)
                for row in pins_reader:
                    res = ProviderResult.from_csv_array(row)
                    results.add(res)

    for name, obj in online_providers.items():
        if name in providers_selected:
            results.add(obj.load(bssid))

    return results


def go(bssid: EUI, essid: str, serial: str, tools_selected: list, providers_selected: list) -> list:
    pins = set()

    if 'all' in providers_selected:
        results = _read_all_db(bssid)
    elif not ('none' in providers_selected):
        results = _read_db(bssid, providers_selected)
    else:
        results = ProviderResults()

    if 'smart' in tools_selected:
        for result in results.results.values():
            pins.update(_get_pins(result, bssid, essid, serial))
    elif 'all' in tools_selected:
        for tool in tools:
            pins.update(tools[tool].get_pins(bssid, essid, serial))
    else:
        for tool in tools:
            if tool in tools_selected:
                pins.update(tools[tool].get_pins(bssid, essid, serial))

    return pins
