from providers.offline.core.helper import *
from providers.online.core.helper import *
from providers.online.downloadable.core.helper import *


def go(csv: bool) -> None:
    if csv:
        print('provider,type')
        for offline_provider in offline_providers.keys():
            print('{},offline'.format(offline_provider))
        for online_provider in online_providers.keys():
            print('{},online'.format(online_provider))
        for online_downloadable_provider in online_downloadable_providers.keys():
            print('{},online_downloadable'.format(online_downloadable_provider))
    else:
        print("Offline providers:\n\033[1m\033[36m- {}\033[0m\n".format('\n- '.join(offline_providers)))
        print("Online queryable providers:\n\033[1m\033[36m- {}\033[0m\n".format('\n- '.join(online_providers)))
        print("Online downloadable providers:\n\033[1m\033[36m- {}\033[0m".format('\n- '.join(online_downloadable_providers)))
