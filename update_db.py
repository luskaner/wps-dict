from os.path import dirname, abspath

from providers.online.downloadable.core.helper import *
from providers.offline.core.helper import *


def go(providers_included: list, providers_excluded: list) -> None:
    pins_path = dirname(abspath(__file__)) + '/pins/'
    providers_db = offline_providers
    providers_db.update(online_downloadable_providers)

    if not ('all' in providers_included) or not ('none' in providers_excluded):
        if not ('none' in providers_excluded):
            providers_db = {key: providers_db[key] for key in (providers_db.keys() - providers_excluded)}
        elif not ('all' in providers_included):
            providers_db = {key: providers_db[key] for key in providers_included}

    for name, obj in providers_db.items():
        res = obj.load_all()
        res.save_as_csv_file(pins_path + name + '.csv')
