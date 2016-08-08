from netaddr import EUI
from os.path import dirname, abspath
import re

from providers.core.results import *
from tools.core.helper import *
from providers.offline.core.helper import *
from providers.online.core.helper import *
from providers.online.downloadable.core.helper import *


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
    path = dirname(abspath(__file__)) + '/pins/'
    results = ProviderResults()

    if providers_db_selected:
        for name, _ in providers_db_selected.items():
            with open(path + name + '.csv', newline='') as csv_file:
                pins_reader = csv.reader(csv_file)
                for _ in range(2):
                    next(pins_reader)
                for row in pins_reader:
                    res = ProviderResult.from_csv_array(row)
                    results.add(res)

    if online_providers_selected:
        for name, obj in online_providers_selected.items():
            res = obj.load(bssid)
            if res:
                results.add(res)

    return results


def go(bssid: EUI, essid: str, serial: str, tools_included: list, tools_excluded: list, providers_included: list,
       providers_excluded: list) -> list:
    pins = set()

    providers_db = offline_providers
    providers_db.update(online_downloadable_providers)
    providers_online = online_providers

    if 'all' in providers_excluded or 'none' in providers_included:
        providers_db = []
        providers_online = []
    elif not ('all' in providers_included) or not ('none' in providers_excluded):
        if providers_excluded:
            for p_excluded in providers_excluded:
                if p_excluded in providers_db:
                    del providers_db[p_excluded]
                elif p_excluded in providers_online:
                    del providers_online[p_excluded]
        elif providers_included:
            tmp_providers_db = []
            tmp_providers_online = []

            for p_included in providers_included:
                if p_included in providers_db:
                    tmp_providers_db[p_included] = providers_db[p_included]
                elif p_included in providers_online:
                    tmp_providers_online[p_included] = providers_online[p_included]

            providers_db = tmp_providers_db
            providers_online = tmp_providers_online

    results = _read_db(bssid, providers_db, providers_online)

    tools_allowed = tools

    if 'all' in tools_excluded or 'none' in tools_included:
        tools_allowed = []
    elif not ('all' in tools_included) or not ('none' in tools_excluded):
        if tools_excluded:
            for t_excluded in tools_excluded:
                if t_excluded in tools_allowed:
                    del tools_allowed[t_excluded]
        elif tools_included:
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

    return pins
