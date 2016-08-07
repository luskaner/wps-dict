from io import StringIO

import requests

from ...core.base import *
from providers.core.results import *


class OfflineProviderGoyScript(DumpProviderBase):
    @staticmethod
    def load_all() -> ProviderResults:
        response = requests.get('https://raw.githubusercontent.com/0x90/wps-scripts/master/goyscript/software/PINs.goy')
        pins_reader = csv.reader(StringIO(response.text), delimiter='-')
        results = ProviderResults()
        for row in pins_reader:
            results.add(ProviderResult(row[0], pins=[row[1]]))
        return results
