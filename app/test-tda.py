from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from .worker.tda_stock import get_recommend_30m


if __name__ == '__main__':
    items = ['NVDA']
    for ticker in items:
        body = get_recommend_30m(ticker)
        print(body)





