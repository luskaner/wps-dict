from netaddr import EUI

from ..helpers.mac import get_ei_int_from_eui
from ..helpers.wps_pin import calc_pin
from .core.base import ToolBase


# Class adapted from ComputePin
# (https://www.wifi-libre.com/topic-9-algoritmo-computepin-c83a35-de-zaochunsheng-la-brecha-en-la-brecha.html)
# Date 4/07/2012
class ToolComputePin(ToolBase):
    @staticmethod
    def get_pins(bssid: EUI, essid: str = None, serial: str = None) -> list:
        ei_int = get_ei_int_from_eui(bssid)
        ei_int_last_seven = ei_int % 10e6
        # noinspection PyTypeChecker
        return [calc_pin(ei_int_last_seven)]

    @staticmethod
    def supported_ouis() -> list:
        return ['C83A35']

    @staticmethod
    def supported_essids() -> list:
        return []

    @staticmethod
    def supported_serials() -> list:
        return []
