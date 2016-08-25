from netaddr import EUI, mac_bare

from helpers.wps_pin import calc_pin
from .core.base import ToolBase


# Class adapted from belkin_pingen (https://github.com/devttys0/wps/blob/master/pingens/belkin/pingen.c)
class ToolBelkinPingen(ToolBase):
    @staticmethod
    def get_pins(bssid: EUI, essid: str, serial: str) -> list:
        if not serial:
            return []

        bssid.dialect = mac_bare
        bssid_str = str(bssid)
        sn = []
        nic = []

        for i in range(1, 5):
            sn.append(int(serial[len(serial) - i], 16))
            nic.append(int(bssid_str[len(bssid_str) - i], 16))

        k1 = (sn[2] + sn[3] + nic[0] + nic[1]) % 16
        k2 = (sn[0] + sn[1] + nic[3] + nic[2]) % 16
        pin = k1 ^ sn[1]
        t1 = k1 ^ sn[0]
        t2 = k2 ^ nic[1]
        p1 = nic[0] ^ sn[1] ^ t1
        p2 = k2 ^ nic[0] ^ t2
        p3 = k1 ^ sn[2] ^ k2 ^ nic[2]
        k1 ^= k2
        pin = (pin ^ k1) * 16

        for num in [t1, p1, t2, p2, k1]:
            pin = (pin + num) * 16

        pin += p3
        pin = (pin % 10e6) - (((pin % 10e6) / 10e6) * k1)
        return [calc_pin(pin)]

    @staticmethod
    def supported_ouis() -> list:
        return []

    @staticmethod
    def supported_essids() -> list:
        return []

    @staticmethod
    def supported_serials() -> list:
        return []
