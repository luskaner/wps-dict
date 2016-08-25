import csv
from copy import deepcopy

from ...helpers import wps_pin
from ...helpers.mac import from_oui_str, get_oui_from_eui


class ProviderResult:
    def __init__(self, starting_mac: str, tools=None, pins=None):
        self.starting_mac = from_oui_str(starting_mac)
        if not self.starting_mac:
            return
        self.tools = set()
        if tools:
            for tool in tools:
                if tool:
                    self.tools.add(tool.lower())
        self.pins_sticker = set()
        self.pins_user = set()
        if pins:
            for pin in pins:
                if len(str(pin)) == 8:
                    if wps_pin.validate(int(pin)):
                        self.pins_sticker.add(pin)
                    else:
                        self.pins_user.add(pin)

    def as_csv_array(self) -> list:
        data = []
        oui = get_oui_from_eui(self.starting_mac)
        data.append(oui)
        data.append('|'.join(self.tools))
        data.append('|'.join(self.pins_sticker))
        data.append('|'.join(self.pins_user))
        return data

    @staticmethod
    def from_csv_array(csv_array):
        starting_mac = csv_array[0]
        tools = csv_array[1].split('|')
        pins = csv_array[2].split('|')
        pins.extend(csv_array[3].split('|'))
        pins = list(filter(None, pins))
        return ProviderResult(starting_mac, tools, pins)


class ProviderResults:
    def __init__(self):
        self.results = {}

    def add(self, provider_result: ProviderResult) -> None:
        mac = provider_result.starting_mac
        if mac:
            if mac in self.results:
                if provider_result.pins_user:
                    self.results[mac].pins_user.update(provider_result.pins_user)
                if provider_result.pins_sticker:
                    self.results[mac].pins_sticker.update(provider_result.pins_sticker)
                if provider_result.tools:
                    self.results[mac].tools.update(provider_result.tools)
            elif (provider_result.pins_sticker or provider_result.pins_user) or provider_result.tools:
                self.results[mac] = provider_result

    def save_as_csv_file(self, path) -> None:
        with open(path, 'w', newline='') as f:
            writer = csv.writer(f)
            '''writer.writerow([
                "# Follows the RFC 4180 (https://tools.ietf.org/html/rfc4180) without quotes using the '|' char to separate elements within columns"])
            '''
            writer.writerow(['oui', 'tools', 'pins_sticker', 'pins_user'])
            for _, res in self.results.items():
                writer.writerow(res.as_csv_array())

    def __add__(self, other):
        ret = deepcopy(self)
        for _, res in other.results.items():
            ret.add(res)
        return ret
