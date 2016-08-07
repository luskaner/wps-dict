from providers.core.results import ProviderResults
from abc import ABC, abstractmethod


class OfflineProviderBase(ABC):
    @staticmethod
    @abstractmethod
    def load_all() -> ProviderResults:
        pass
