from tools.core.helper import *


def go(csv: bool) -> None:
    if csv:
        print('tool')
        print('\n'.join(tools))
    else:
        print('Tools:\n\033[1m\033[36m- {}\033[0m'.format('\n- '.join(tools)))
