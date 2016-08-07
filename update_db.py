from os.path import dirname, abspath

from providers.offline import *


def go() -> None:
    pins_path = dirname(abspath(__file__)) + '/pins/pins.csv'

    offline_providers = [
        wps_bunker.OfflineProviderWpsBunker,
        download_wireless_net.OfflineProviderDownloadWirelessNet,
        goy_script.OfflineProviderGoyScript
    ]

    res = offline_providers[0].load_all()
    for i in range(1, len(offline_providers)):
        res += offline_providers[i].load_all()

    res.save_as_csv_file(pins_path)
