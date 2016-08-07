from netaddr import EUI

from helpers.mac import get_ei_from_eui
from helpers.wps_pin import calc_pin
from .core.base import ToolBase


# Class adapted from tdn.sh (https://github.com/kcdtv/tdn/blob/master/tdn.sh)
# Date 25 June 2015
class ToolTdnSh(ToolBase):
    @staticmethod
    def get_pins(bssid: EUI, essid: str = None, serial: str = None) -> list:
        ei = get_ei_from_eui(bssid)
        ei_reverse = ei[4:6] + ei[2:4] + ei[0:2]
        return [calc_pin(int(ei_reverse, 16) % 10e6)]

    @staticmethod
    def supported_ouis() -> list:
        return ['D8EB97', '0014D1', '3C8CF8']

    @staticmethod
    def supported_essids() -> list:
        return []

    @staticmethod
    def supported_serials() -> list:
        return []
