from os.path import dirname, abspath

from providers.online.downloadable.core.helper import *
from providers.offline.core.helper import *


def go() -> None:
    pins_path = dirname(abspath(__file__)) + '/pins/'
    offline_providers.update(online_downloadable_providers)
    for name, obj in offline_providers.items():
        res = obj.load_all()
        res.save_as_csv_file(pins_path + name + '.csv')
