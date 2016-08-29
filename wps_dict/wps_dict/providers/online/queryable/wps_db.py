import requests
from pyquery import PyQuery as Pq
from netaddr import EUI

from ....helpers.mac import get_oui_from_eui
from .core.base import OnlineQueryableProviderBase
from ...core.results import ProviderResult


class ProviderWpsDb(OnlineQueryableProviderBase):
    @staticmethod
    def load(bssid: EUI) -> ProviderResult:
        mac_oui = get_oui_from_eui(bssid)
        params = {'abuscaren': 'MAC', 'busqueda': mac_oui, 'BUSCAR': 'Buscar'}
        response = requests.post('http://wpsdb.site40.net/consulta.php', params)
        d = Pq(response.text)
        pin_cells = d('table.table tr td:eq(1)')
        pins = set()
        for cell in pin_cells:
            try:
                pin = str(int(cell.text))
                pins.add(pin)
            except ValueError:
                continue
        if pins:
            return ProviderResult(mac_oui, pins=pins)
        else:
            return None
