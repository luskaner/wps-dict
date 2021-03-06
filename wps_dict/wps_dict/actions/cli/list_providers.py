from ...providers.online.downloadable.list import online_downloadable_providers
from ...providers.online.queryable.list import online_queryable_providers
from ...providers.offline.list import offline_providers


def go(csv: bool) -> None:
    if csv:
        print('provider,type')
        for offline_provider in offline_providers.keys():
            print('{},offline'.format(offline_provider))
        for online_provider in online_queryable_providers.keys():
            print('{},online_queryable'.format(online_provider))
        for online_downloadable_provider in online_downloadable_providers.keys():
            print('{},online_downloadable'.format(online_downloadable_provider))
    else:
        print("Offline providers:\n\033[1m\033[36m- {}\033[0m\n".format('\n- '.join(offline_providers)))
        print("Online providers:".format('\n- '.join(online_queryable_providers)))
        print("* Queryable providers:\n\033[1m\033[36m- {}\033[0m\n".format('\n- '.join(online_queryable_providers)))
        print("* Downloadable providers:\n\033[1m\033[36m- {}\033[0m".format(
            '\n- '.join(online_downloadable_providers)))
