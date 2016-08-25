from netaddr import EUI
from abc import ABC, abstractmethod


class ToolBase(ABC):
    # For the supported_* functions, regex is used
    @staticmethod
    @abstractmethod
    def supported_ouis() -> list:
        pass

    @staticmethod
    @abstractmethod
    def supported_essids() -> list:
        pass

    @staticmethod
    @abstractmethod
    def supported_serials() -> list:
        pass

    @staticmethod
    @abstractmethod
    def get_pins(bssid: EUI, essid: str = None, serial: str = None) -> list:
        pass
