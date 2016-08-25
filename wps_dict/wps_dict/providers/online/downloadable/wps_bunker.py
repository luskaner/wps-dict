from io import StringIO

import requests

from ...core.base import *
from ....providers.core.results import *


class OfflineProviderWpsBunker(DumpProviderBase):
    @staticmethod
    def load_all() -> ProviderResults:
        response = requests.get('http://wpsbunker.hackaffeine.com/download_wps_db.php')
        reader = csv.reader(StringIO(response.text))
        for _ in range(2):
            next(reader)
        results = ProviderResults()
        for row in reader:
            starting_mac = "{}:{}:{}".format(row[0][0:2], row[0][2:4], row[0][4:6])
            results.add(ProviderResult(starting_mac, [None], [row[1]]))
        return results
