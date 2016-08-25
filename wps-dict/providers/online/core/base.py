from providers.core.results import ProviderResults
from netaddr import EUI
from abc import ABC, abstractmethod


class OnlineProviderBase(ABC):
    @staticmethod
    @abstractmethod
    def load(mac: EUI) -> ProviderResults:
        pass
