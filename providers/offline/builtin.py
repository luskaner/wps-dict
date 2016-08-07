from ..core.base import *
from providers.core.results import *


class OfflineProviderBuiltin(DumpProviderBase):
    @staticmethod
    def load_all() -> ProviderResults:
        results = ProviderResults()
        results.add(ProviderResult('000000', pins=[00000000]))
        return results
