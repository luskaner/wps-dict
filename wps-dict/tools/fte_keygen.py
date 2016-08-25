import re

from helpers.mac import get_ei_from_eui, get_oui_from_eui
from .compute_pin import *
from .core.base import ToolBase


# Class adapted from WPSPinGeneratorMOD (https://github.com/0x90/wps-scripts/blob/master/goyscript/software/WPSPinGeneratorMOD)
# Date 4 May 2015
class ToolFteKeygen(ToolBase):
    @staticmethod
    def get_pins(bssid: EUI, essid: str, serial: str = None) -> list:
        ei = get_ei_from_eui(bssid)
        ei_int = int(ei, 16)
        ei_int_last_seven = ei_int % 10e6
        match = re.search('^FTE-(\d{4})$', essid)
        if match:
            concat = int(str(ei)[:2] + match.group(1), 16)
            last_seven = concat % 10e6
            return [calc_pin(last_seven, 7)]
        else:
            oui = get_oui_from_eui(bssid)
            pins = []
            if oui in ToolFteKeygen.supported_ouis():
                pins.append(calc_pin(ei_int_last_seven, 8))
                pins.append(calc_pin(ei_int_last_seven, 14))
        pins.extend(ToolComputePin.get_pins(bssid))
        return pins

    @staticmethod
    def supported_ouis() -> list:
        return ['04C06F', '202BC1', '80B686', '84A8E4', 'B4749F', 'BC7670', 'CC96A0', 'F83DFF']

    @staticmethod
    def supported_essids() -> list:
        return ['FTE-\d{4}']

    @staticmethod
    def supported_serials() -> list:
        return []
