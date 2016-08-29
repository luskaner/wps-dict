from netaddr import EUI
from abc import ABC, abstractmethod
from ....core.results import ProviderResults


class OnlineQueryableProviderBase(ABC):
    @staticmethod
    @abstractmethod
    def load(mac: EUI) -> ProviderResults:
        pass
