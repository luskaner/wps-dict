from ..core.base import DumpProviderBase
from ...providers.core.results import ProviderResult, ProviderResults


class ProviderBuiltin(DumpProviderBase):
    @staticmethod
    def load_all() -> ProviderResults:
        results = ProviderResults()
        results.add(ProviderResult('123456', pins=['12345678']))
        return results
