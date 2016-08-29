from io import StringIO

import requests
import csv

from ...core.base import DumpProviderBase
from ....providers.core.results import ProviderResult, ProviderResults


class ProviderDownloadWirelessNet(DumpProviderBase):
    @staticmethod
    def load_all() -> ProviderResults:
        response = requests.get('http://www.downloadwireless.net/scripts-live/patrones_conocidos.txt')
        reader = csv.reader(StringIO(response.text), delimiter='\t')
        for _ in range(4):
            next(reader)
        results = ProviderResults()
        for row in reader:
            row = list(filter(None, row))
            if row and (row[1].lower() == 'wps' and row[2].lower() != 'pixiewps'):
                starting_mac = row[0]
                tool = None
                pins = None
                if row[2].lower() != 'pingenerico':
                    tool = row[2].replace('.py', '')
                else:
                    pins = str.split(row[4])
                results.add(ProviderResult(starting_mac, [tool], pins))
        return results
