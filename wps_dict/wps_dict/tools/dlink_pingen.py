from netaddr import EUI

from ..helpers.mac import get_ei_int_from_eui
from ..helpers.wps_pin import wps_pin_checksum
from .core.base import ToolBase


#  Class adapted from dlink_pingen.py (https://github.com/devttys0/wps/blob/master/pingens/dlink/pingen.py)
#  Date: 1 Nov 2014
class ToolDlinkPingen(ToolBase):
    @staticmethod
    def get_pins(bssid: EUI, essid: str = None, serial: str = None) -> list:
        ei_int = get_ei_int_from_eui(bssid)
        pin = ei_int ^ 0x55AA55
        pin ^= (((pin & 0x0F) << 4) +
                ((pin & 0x0F) << 8) +
                ((pin & 0x0F) << 12) +
                ((pin & 0x0F) << 16) +
                ((pin & 0x0F) << 20))

        # The largest possible remainder for any value divided by 10,000,000
        # is 9,999,999 (7 digits). The smallest possible remainder is, obviously, 0.
        pin %= int(10e6)

        # If the pin is less than 1,000,000 (i.e., less than 7 digits)
        if pin < int(10e5):
            # The largest possible remainder for any value divided by 9 is
            # 8; hence this adds at most 9,000,000 to the pin value, and at
            # least 1,000,000. This guarantees that the pin will be 7 digits
            # long, and also means that it won't start with a 0.
            pin += (pin % 9) * int(10e5) + int(10e5)

        # The final 8 digit pin is the 7 digit value just computed, plus a
        # checksum digit.
        return [pin * 10 + wps_pin_checksum(pin)]

    @staticmethod
    def supported_ouis() -> list:
        return []

    @staticmethod
    def supported_essids() -> list:
        return []

    @staticmethod
    def supported_serials() -> list:
        return []
