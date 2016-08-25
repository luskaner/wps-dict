from ..core.base import *
from ...providers.core.results import *


class OfflineProviderBuiltin(DumpProviderBase):
    @staticmethod
    def load_all() -> ProviderResults:
        results = ProviderResults()
        # results.add(ProviderResult('123456', pins=['12345678']))
        return results
