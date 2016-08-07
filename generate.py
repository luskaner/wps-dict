from netaddr import EUI
from os.path import dirname, abspath
import csv
import re

from helpers.mac import get_oui_from_eui
from providers.core.results import ProviderResult
from providers.online import *
from tools.core.helper import *

online_providers = [
    wps_db.OnlineProviderWpsDb
]


def _get_pins(res: ProviderResult, bssid: EUI, essid: str, serial: str, all_tools: bool) -> list:
    pins = set()
    oui_bssid = get_oui_from_eui(res.starting_mac)

    tools_run = set()
    if oui_bssid == get_oui_from_eui(bssid):
        pins.update(res.pins_sticker)
        pins.update(res.pins_user)
        for tool in res.tools:
            if tool in tools_matcher and tool != 'COMPUTEPIN':
                pins.update(tools_matcher[tool].get_pins(bssid, essid, serial))
                tools_run.update([tool])

        for online_provider in online_providers:
            res_tmp = online_provider.load(bssid)
            if res_tmp:
                pins.update(res_tmp.pins_sticker)
                pins.update(res_tmp.pins_user)

    for tool in tools_matcher:
        if not (tool in tools_run) and tool != 'COMPUTEPIN':
            if oui_bssid in tools_matcher[tool].supported_ouis():
                pins.update(tools_matcher[tool].get_pins(bssid, essid, serial))
            else:
                essids = tools_matcher[tool].supported_essids()
                serials = tools_matcher[tool].supported_serials()
                if essid and essids:
                    for e in essids:
                        if re.match(e, essid):
                            pins.update(tools_matcher[tool].get_pins(bssid, essid, serial))
                elif serial and serials:
                    for s in serials:
                        if re.match(s, serial):
                            pins.update(tools_matcher[tool].get_pins(bssid, essid, serial))
    return pins


def go(bssid: EUI, essid: str, serial: str, all_tools: bool) -> list:
    pins = set()
    with open(dirname(abspath(__file__)) + '/pins/pins.csv', newline='') as csv_file:
        pins_reader = csv.reader(csv_file)
        for _ in range(2):
            next(pins_reader)
        for row in pins_reader:
            res = ProviderResult.from_csv_array(row)
            pins.update(_get_pins(res, bssid, essid, serial, all_tools))
        pins.update(tools_matcher['COMPUTEPIN'].get_pins(bssid, essid, serial))
        if all_tools:
            del tools_matcher['COMPUTEPIN']
            for tool in tools_matcher:
                pins.update(tools_matcher[tool].get_pins(bssid, essid, serial))
    return pins
