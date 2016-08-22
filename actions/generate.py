from netaddr import EUI
from os.path import dirname, abspath
import re
import os.path

from providers.core.results import *
from tools.core.helper import *
from providers.offline.core.helper import *
from providers.online.core.helper import *
from providers.online.downloadable.core.helper import *
from helpers.internet_connection import is_connected

error_code = 0


def _get_pins(res: ProviderResult, bssid: EUI, essid: str, serial: str, tools_allowed: list) -> list:
    pins = set()
    oui_bssid = get_oui_from_eui(res.starting_mac)
    tools_run = set()

    if oui_bssid == get_oui_from_eui(bssid):
        pins.update(res.pins_sticker)
        pins.update(res.pins_user)
        for tool in tools_allowed:
            if tool in tools_allowed:
                pins.update(tools_allowed[tool].get_pins(bssid, essid, serial))
                tools_run.update([tool])

    for tool in tools_allowed:
        if not (tool in tools_run):
            if oui_bssid in tools_allowed[tool].supported_ouis():
                pins.update(tools_allowed[tool].get_pins(bssid, essid, serial))
            else:
                essids = tools_allowed[tool].supported_essids()
                serials = tools_allowed[tool].supported_serials()
                if essid and essids:
                    for e in essids:
                        if re.match(e, essid):
                            pins.update(tools_allowed[tool].get_pins(bssid, essid, serial))
                elif serial and serials:
                    for s in serials:
                        if re.match(s, serial):
                            pins.update(tools_allowed[tool].get_pins(bssid, essid, serial))
    return pins


def _read_db(bssid: EUI, providers_db_selected: list, online_providers_selected: list) -> ProviderResults:
    path = dirname(abspath(__file__)) + '/../pins/'
    results = ProviderResults()

    if providers_db_selected:
        for name, _ in providers_db_selected.items():
            file_path = path + name + '.csv'
            if os.path.exists(file_path):
                with open(file_path, newline='') as csv_file:
                    pins_reader = csv.reader(csv_file)
                    for _ in range(1):
                        next(pins_reader)
                    for row in pins_reader:
                        res = ProviderResult.from_csv_array(row)
                        results.add(res)

    if online_providers_selected:
        if is_connected():
            for name, obj in online_providers_selected.items():
                res = obj.load(bssid)
                if res:
                    results.add(res)
        else:
            print('\033[1m\033[33mWARNING: Online providers will not be checked without internet connection\033[0m')
            global error_code
            error_code = 3

    return results


def go(bssid: EUI, essid: str, serial: str, tools_included: list, tools_excluded: list, providers_included: list,
       providers_excluded: list) -> (list, int):
    pins = set()

    providers_db = offline_providers
    providers_db.update(online_downloadable_providers)
    providers_online = online_providers

    if 'all' in providers_excluded or 'none' in providers_included:
        providers_db = []
        providers_online = []
    elif not ('all' in providers_included) or not ('none' in providers_excluded):
        if not ('none' in providers_excluded):
            providers_db = {key: providers_db[key] for key in (providers_db.keys() - providers_excluded) if
                            key in providers_db}
            providers_online = {key: providers_online[key] for key in (providers_online.keys() - providers_excluded) if
                                key in providers_online}
        elif not ('all' in providers_included):
            providers_db = {key: providers_db[key] for key in providers_included if key in providers_db}
            providers_online = {key: providers_online[key] for key in providers_online if key in providers_online}

    results = _read_db(bssid, providers_db, providers_online)

    tools_allowed = tools

    if ('all' in tools_excluded or 'none' in tools_included) or ('auto' in tools_excluded and 'auto' in tools_included):
        tools_allowed = []
    elif not ('all' in tools_included) or not ('none' in tools_excluded):
        if not ('none' in tools_excluded):
            for t_excluded in tools_excluded:
                if t_excluded in tools_allowed:
                    del tools_allowed[t_excluded]
        elif not ('all' in tools_included):
            tmp_tools_allowed = []

            for t_included in tools_included:
                if t_included in tools_allowed:
                    tmp_tools_allowed[t_included] = tools_allowed[t_included]

            tools_allowed = tmp_tools_allowed

    if providers_db or providers_online:
        for result in results.results.values():
            pins.update(_get_pins(result, bssid, essid, serial, tools_allowed))
    else:
        for tool in tools_allowed:
            pins.update(tools_allowed[tool].get_pins(bssid, essid, serial))

    return [str(pin) for pin in pins], error_code
